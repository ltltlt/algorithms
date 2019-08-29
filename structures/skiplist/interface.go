package skiplist

// OrderedSet is a set with order
// It doesn't matter if element can or cannot compared
// element order is specified by score. Just like zset in redis.
type OrderedSet interface {
	IsSet(score float64) bool
	Set(score float64, value interface{}) bool
	Del(score float64) bool
	Get(score float64) (interface{}, bool)
	// Set or Del during ForEach is unspecified
	ForEach(func(float64, interface{}))
	// Collect values into a slice, this will be ordered by score
	Collect() []interface{}
	Len() int
	Dump() string
}

// New creates an OrderedSet
func New() OrderedSet {
	return newSkiplist(4)
}
