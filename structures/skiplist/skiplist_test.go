package skiplist_test

import (
	"math/rand"
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"

	"cytus2.rocks/skiplist"
)

func TestSet(t *testing.T) {
	assert := assert.New(t)
	var zset = skiplist.New()
	var slice = []interface{}{-12, "122s", 2.1, 2 - 1i, []int{1, 2}, -1, -3, -1, -333}
	for i, v := range slice {
		assert.Equalf(zset.Len(), i, "len [%d %d] fail", i, zset.Len())
		assert.Equalf(zset.Set(float64(i), v), true, "set [%d %+v] fail", i, v)
		assert.Equalf(zset.IsSet(float64(i)), true, "isset [%d %+v] fail", i, v)
		v1, _ := zset.Get(float64(i))
		assert.Equalf(reflect.DeepEqual(v1, v), true, "get [%d %+v %+v] fail", i, v, v1)
	}
	var slice1 = zset.Collect()
	assert.Equalf(reflect.DeepEqual(slice, slice1), true, "collect [%+v %+v] fail", slice, slice1)
	for i, v := range slice {
		assert.Equalf(zset.Del(float64(i)), true, "del [%d %+v] fail", i, v)
		v, ok := zset.Get(float64(i))
		assert.Equalf(ok, false, "del get [%d %+v] fail", i, v)
	}
	assert.Equalf(zset.Len(), 0, "del len [%+v] fail", slice1)
}

func TestRandom(t *testing.T) {
	assert := assert.New(t)
	sl := skiplist.New()
	var count uint32 = 10000
	for i := 0; i < 100000; i++ {
		score := float64(rand.Uint32() % count)
		assert.Equalf(sl.IsSet(score), !sl.Set(score, 1), "add fail: [%d %.0f]", i, score)
	}
	assert.Truef(int(count) >= sl.Len(), "len fail: [%d %d]", count, sl.Len())
	for i := 0; i < 100000; i++ {
		score := float64(rand.Uint32() % count)
		assert.Equalf(sl.IsSet(score), sl.Del(score), "del fail: [%d %.0f]", i, score)
	}
}

func TestDuplicate(t *testing.T) {
	assert := assert.New(t)
	sl := skiplist.New()
	for i := 0; i < 100000; i++ {
		assert.Equalf((i == 0) == sl.Set(2, i), true, "add [%d] fail", i)
	}
	assert.Equalf(sl.Len(), 1, "duplicate fail with len: %d", sl.Len())
	assert.Equalf(sl.Del(2), true, "del 2 fail")
	assert.Equalf(sl.Len(), 0, "del len fail with len: %d", sl.Len())
}
