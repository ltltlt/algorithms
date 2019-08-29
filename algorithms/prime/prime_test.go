package prime

import (
	"math"
	"testing"

	"github.com/stretchr/testify/assert"
)

func upTo(n int) []int {
	var result []int
	for i := 2; i <= n; i++ {
		root := int(math.Sqrt(float64(i)))
		isPrime := true
		for j := 2; j <= root; j++ {
			if i%j == 0 {
				isPrime = false
				break
			}
		}
		if isPrime {
			result = append(result, i)
		}
	}
	return result
}

func TestUnder(t *testing.T) {
	for i := 0; i < 10000; i++ {
		assert.ElementsMatch(t, upTo(i), UpTo(i))
	}
}

func BenchmarkUnder(b *testing.B) {
	for i := 0; i < b.N; i++ {
		UpTo(10000)
	}
}
