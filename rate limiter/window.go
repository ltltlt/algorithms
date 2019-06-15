package rate_limiter

import (
	"container/list"
	"sync"
	"time"
)

type RateLimiter4 struct {
	size       int
	current    int
	windowSize int
	windows    *list.List
	mu         sync.Mutex
}

// size is the max qps you want
func NewRateLimiter4(size, windowSize int) *RateLimiter4 {
	windows := list.New()
	for i := 0; i < windowSize; i++ {
		windows.PushBack(0)
	}
	rl := &RateLimiter4{
		size:    size,
		current: 0,
		windows: windows,
	}

	go func() {
		for {
			rl.mu.Lock()
			front := rl.windows.Front()
			rl.current += front.Value.(int)
			rl.windows.Remove(front)
			rl.windows.PushBack(0)
			rl.mu.Unlock()

			time.Sleep(time.Second / time.Duration(windowSize))
		}
	}()

	return rl
}

func (rl *RateLimiter4) Acquire(n int) {
	for {
		rl.mu.Lock()
		if rl.current+n <= rl.size {
			break
		}
		rl.mu.Unlock()
		time.Sleep(time.Second / time.Duration(rl.windowSize))
	}
	rl.windows.Back().Value = rl.windows.Back().Value.(int) + n
	rl.current += n
	rl.mu.Unlock()
}
