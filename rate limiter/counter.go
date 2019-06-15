package rate_limiter

import (
	"sync"
	"time"
)

type RateLimiter2 struct {
	count      int
	current    int
	ratePerSec int
	mu         sync.Mutex
	utime      time.Time
}

func NewRateLimiter2(size int, ratePerSec int) *RateLimiter2 {
	return &RateLimiter2{
		count:      size,
		current:    size,
		ratePerSec: ratePerSec,
	}
}

func (rl *RateLimiter2) Acquire(n int) {
	if n >= rl.count {
		panic("way too much to acquire")
	}

	var ct time.Time
	var nc int
	for {
		ct = time.Now()
		rl.mu.Lock()
		duration := ct.Sub(rl.utime)

		nc = min(
			rl.ratePerSec*int(duration.Seconds())+rl.current-n,
			rl.count,
		)
		if nc >= 0 {
			break
		}
		rl.mu.Unlock()
		time.Sleep(time.Second * time.Duration(-nc/rl.ratePerSec))
	}
	rl.utime = ct
	rl.current = nc
	rl.mu.Unlock()
}

func min(i, j int) int {
	if i < j {
		return i
	}
	return j
}
