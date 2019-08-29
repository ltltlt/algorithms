package skiplist

import (
	"math/rand"
	"time"
)

type random interface {
	// generate random variable between [0, max)
	random(max int) int
}

// p=1/2 geometric distribution
type geometricDistribution struct {
}

func (geometricDistribution) random(max int) int {
	source := rand.NewSource(time.Now().UnixNano())
	r := rand.New(source)
	number := 0
	for r.Intn(2) == 0 && number < max-1 {
		number++
	}
	return number
}
