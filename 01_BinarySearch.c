/* Aim: To implement Binary Search using
        i) Iterative Method
        ii) Recursion Method

Algorithm:
Binary_Search(a, low, high, val) // 'a' is the given array, 'low' is the index of the first array element, 'high' is the index of the last array element, 'val' is the value to search  
Step 1: set beg = low, end = high, pos = - 1  
Step 2: repeat steps 3 and 4 while beg <=end  
Step 3: set mid = (beg + end)/2  
Step 4: if a[mid] = val  
set pos = mid  
print pos  
go to step 6  
else if a[mid] > val  
set end = mid - 1  
else  
set beg = mid + 1  
[end of if]  
[end of loop]  
Step 5: if pos = -1  
print "value is not present in the array"  
[end of if]  
Step 6: exit 
*/
/*Iterative*/
#include <stdio.h>
int main ()
{
  printf ("Name : __________ \nEnrollment No. :  _____________ \n\n"); // Fill the blanks as per your own convenience
  int i, low, high, mid, n, key, array[100];
  printf ("Enter number of elements:");
  scanf ("%d", &n);
  printf ("Enter %d integers in ascending order:", n);
  for (i = 0; i < n; i++)
    scanf ("%d", &array[i]);
  printf ("Enter value to find:");
  scanf ("%d", &key);
  low = 0;
  high = n - 1;
  mid = (low + high) / 2;
  while (low <= high)
    {
      if (array[mid] < key)
	low = mid + 1;
      else if (array[mid] == key)
	{
	  printf ("%d found at location %d.", key, mid + 1);
	  break;
	}
      else
	high = mid - 1;
      mid = (low + high) / 2;
    }
  if (low > high)
    printf ("Not found! %d isn't present in the list.", key);
  return 0;
}

/*Recursive*/
