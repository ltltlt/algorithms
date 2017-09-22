/*************************************************************************
	> File Name:		StringSort.cpp
	> Author:			ty-l8
	> Mail:				liuty196888@gmail.com
	> Created Time:		2017-09-22 Fri 19:10
 ************************************************************************/

#include <iostream>
#include <string>
#include <vector>
#include <random>
#include <string.h>
#include <algorithm>
using namespace std;

class Quick3String{
public:
	void quick3string(vector<string> &array){
		quick3string(array, 0, array.size()-1, 0);
	}
private:
	static int getChar(string &str, int d){
		if (d>=(int)str.length()) return -1;
		return str[d];
	}
	static void swap(string &a, string &b){
		string tmp = std::move(a);
		a = std::move(b);
		b = std::move(tmp);
	}
	static void quick3string(vector<string> &array, int low, int high, int d){
		// sort array[low, high](include bounds)
		if (low>=high) return;
		// in quicksort, we split array into two part, so we only need one point, but now we split it into 3 parts, hence two point is what we need
		// i always point to current element need to process
		// lt always point to the first element startswith key and all element before is smaller than this
		// findally gt will point to the element which is previous the first element is larger than k
		int lt = low, gt = high, i = low+1;
		int key = getChar(array[low], d);
		while (i<=gt) {		// runs exactly high-low times, each element will process once
			int k = getChar(array[i], d);
			if (k>key)
				swap(array[i], array[gt--]);	// we cannot i++ here because array[i] is new and not be processed
			else if (k<key)
				swap(array[i++], array[lt++]);	// even though array[i] is new, but we must process it before
			else
				i += 1;
		}
		quick3string(array, low, lt-1, d);
		if (key>=0)
			quick3string(array, lt, gt, d+1);
		quick3string(array, gt+1, high, d);
	}
};
void test(){
	std::random_device rd;
	vector<string> vec1, vec2;
	char str[100];
	const char *chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWEYZ1234567890-=_+|{}[]()\"\';:,.<>/?~`";
	int char_len = strlen(chars);
	for (int i=0; i<10000; i+=1){
		int length = rd()%100;
		int j;
		for (j=0; j<length; j+=1)
			str[j] = chars[rd()%char_len];
		vec1.emplace_back(str, str+length);
		vec2.emplace_back(str, str+length);
	}
	sort(vec1.begin(), vec1.end());
	Quick3String q3s;
	q3s.quick3string(vec2);
	bool flag = true;
	for (size_t i=0; i<vec1.size(); i+=1)
		if (vec1[i]!=vec2[i]){
			flag = false;
			break;
		}
	std::cout << std::boolalpha << flag << std::endl;
}
int main(void)
{
	test();
	return 0;
}
