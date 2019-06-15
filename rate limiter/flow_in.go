package rate_limiter

import (
	"time"
)

type RateLimiter struct {
	bucket chan struct{}
}

func NewRateLimiter(size int, ratePerSec int) *RateLimiter {
	bucket := make(chan struct{}, size)
	go func() {
		for {
			for i := 0; i < ratePerSec; i++ {
				select {
				case bucket <- struct{}{}:
				default: // bucker is full, wait for next time
					break
				}
			}
			time.Sleep(time.Second)
		}
	}()
	return &RateLimiter{
		bucket: bucket,
	}
}

func (rl *RateLimiter) Acquire(n int) {
	for i := 0; i < n; i++ {
		<-rl.bucket
	}
}
