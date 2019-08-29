package prime

// UpTo search prime up to(include) n
// use algorithm Sieve of Eratosthenes
func UpTo(n int) []int {
	if n < 2 {
		return nil
	}
	if n == 2 {
		return []int{2}
	}
	// prime true, or false
	// lets filter composite number out
	// use extra 1 byte to make things clear
	var slice = make([]bool, n+1)
	for i := 2; i < n+1; i++ {
		slice[i] = true
	}
	for i := 2; i < n+1; i++ {
		if slice[i] {
			for j := i << 1; j < n+1; j += i {
				slice[j] = false
			}
		}
	}
	var result []int
	for i := 2; i < n+1; i++ {
		if slice[i] {
			result = append(result, i)
		}
	}
	return result
}
