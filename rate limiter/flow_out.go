package rate_limiter

import "time"

type RateLimiter3 struct {
	bucket chan struct{}
}

func NewRateLimiter3(size int, ratePerSec int) *RateLimiter3 {
	bucket := make(chan struct{}, size)
	go func() {
		for {
			for i := 0; i < ratePerSec; i++ {
				select {
				case <-bucket:
				default:
					break
				}
			}
			time.Sleep(time.Second)
		}
	}()
	return &RateLimiter3{
		bucket: bucket,
	}
}

func (rl *RateLimiter3) Acquire(n int) {
	for i := 0; i < n; i++ {
		rl.bucket <- struct{}{}
	}
}
