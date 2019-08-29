package skiplist

import (
	"fmt"
	"io"
	"strings"
)

// this version only avoid duplicate score(key), next version i will accept it
type skiplist struct {
	maxLevel int

	head node // head doesn't store data
	size int
}

type node struct {
	level int // this node's highest level
	value interface{}
	score float64
	nexts []*node
}

func newSkiplist(maxlevel int) *skiplist {
	if maxlevel <= 0 {
		panic("max level should larger than 0")
	}
	return &skiplist{
		maxLevel: maxlevel,
		head: node{
			level: maxlevel,
			nexts: make([]*node, maxlevel),
		},
	}
}

func (sl *skiplist) IsSet(score float64) bool {
	_, ok := sl.Get(score)
	return ok
}

// Set a value into skiplist
// if a new node created, return true, else return false(update)
// O(level * log n)
func (sl *skiplist) Set(score float64, value interface{}) bool {
	level := 1 + geometricDistribution{}.random(sl.maxLevel) // this node can exist at most at level [0, level)
	// previous[i] stores in level i, new node's previous node
	var previous = make([]*node, sl.maxLevel)
	var current = &sl.head
	for i := sl.maxLevel - 1; i >= 0; i-- {
		for current.nexts[i] != nil && current.nexts[i].score < score {
			current = current.nexts[i]
		}
		if current.nexts[i] != nil && current.nexts[i].score == score {
			current.nexts[i].value = value
			return false
		}
		previous[i] = current
	}
	newn := &node{
		level: level,
		score: score,
		value: value,
		nexts: make([]*node, level),
	}
	for i, n := range previous[:level] {
		newn.nexts[i] = n.nexts[i]
		n.nexts[i] = newn
	}
	sl.size++
	return true
}

// Get the random value in this skiplist has that score, there's no way for two different value have the same score
// O(level * log n)
func (sl *skiplist) Get(score float64) (interface{}, bool) {
	var current = &sl.head
	for i := sl.maxLevel - 1; i >= 0; i-- {
		// index will never out-of-bound because current.level > i always satisfy
		// in level i, you cannot access node which level <= i
		for current.nexts[i] != nil && current.nexts[i].score < score {
			current = current.nexts[i]
		}
		if current.nexts[i] != nil && current.nexts[i].score == score {
			return current.nexts[i].value, true
		}
	}
	return nil, false
}

// O(level * log n)
func (sl *skiplist) Del(score float64) bool {
	var previous = make([]*node, sl.maxLevel)
	var current = &sl.head
	for i := sl.maxLevel - 1; i >= 0; i-- {
		for current.nexts[i] != nil && current.nexts[i].score < score {
			current = current.nexts[i]
		}
		if current.nexts[i] != nil && current.nexts[i].score == score {
			previous[i] = current
		}
	}
	del := false
	for i, n := range previous {
		if n == nil {
			break
		}
		del = true
		previous[i].nexts[i] = previous[i].nexts[i].nexts[i]
	}
	if del {
		sl.size--
	}
	return del
}

// O(n)
func (sl *skiplist) ForEach(f func(float64, interface{})) {
	for node := sl.head.nexts[0]; node != nil; node = node.nexts[0] {
		f(node.score, node.value)
	}
}

func (sl *skiplist) Collect() []interface{} {
	var results []interface{}
	sl.ForEach(func(_ float64, value interface{}) {
		results = append(results, value)
	})
	return results
}

func (sl *skiplist) Len() int {
	return sl.size
}

func (sl *skiplist) Dump() string {
	writer := &strings.Builder{}
	fmt.Fprintf(writer, "level: %d, size: %d\n", sl.maxLevel, sl.size)
	for level := 0; level < sl.maxLevel; level++ {
		sl.dumpLevel(writer, level)
	}
	return writer.String()
}

func (sl *skiplist) dumpLevel(writer io.Writer, level int) {
	fmt.Fprintf(writer, "level(%d): ", level)
	formatter := "(%.2f %+v) "
	for l0node, n := sl.head.nexts[0], sl.head.nexts[level]; n != nil; l0node, n = l0node.nexts[0], n.nexts[level] {
		for l0node != n {
			l0node = l0node.nexts[0]
			padding := strings.Repeat(" ", len(fmt.Sprintf(formatter, l0node.score, l0node.value)))
			fmt.Fprintf(writer, padding)
		}
		fmt.Fprintf(writer, formatter, n.score, n.value)
	}
	fmt.Fprintln(writer)
}
