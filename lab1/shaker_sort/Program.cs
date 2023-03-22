using System;
using System.Diagnostics;
using System.IO;

namespace shaker_sort
{
    class Program
    { 
        static void Main(string[] args)
        {
            int items = 1000;
            for (int i = 0; i < 8; i++)
            {
                Sort sort = new Sort(items);
                items *= 2;
            }
            Console.WriteLine("End sort");
        }
    }

    class Sort
    {
        public Sort(int N)
        {
            analysis(N);
        }
        static double[] array;
        static double[] generateArray(int N)
        {
            array = new double[N];
            int max = -1;
            int min = 1;
            Random rnd = new Random();
            for (int i = 0; i < N; i++)
            {
                array[i] = rnd.NextDouble() * (max - min) + min;
            }
            return array;
        }

        static double shakerSort(int N)
        {
            double[] arr = generateArray(N);
            Stopwatch time = new Stopwatch();
            time.Start();
            int left = 0;
            int right = arr.Length - 1;
            do
            {
                for (int i = left; i < right; i++)
                {
                    if (arr[i] > arr[i + 1])
                    {
                        swap(ref arr[i], ref arr[i + 1]);
                    }
                }
                right--;
                for (int i = left; i > right; i--)
                {
                    if (arr[i] > arr[i - 1])
                    {
                        swap(ref arr[i], ref arr[i + 1]);
                    }
                }
                left++;
            }
            while (left <= right);
            time.Stop();
            return time.ElapsedMilliseconds;
        }

        static void analysis(int N)
        {
            double min_value = -1;
            double max_value = 0;
            int count_analysis = 20;
            double[] average = new double[count_analysis];
            for (int i = 0; i < count_analysis; i++)
            {
                double res = shakerSort(N);
                if (min_value == -1)
                    min_value = res;
                if (res > max_value)
                {
                    max_value = res;
                }
                if (res < min_value)
                {
                    min_value = res;
                }
                average[i] = res;
            }
            double avg = averageArray(average);
            Console.WriteLine("Elements:" + N + " min: " + min_value + " max: " + max_value + " avg: " + avg + "\n");
            using (StreamWriter writer = new StreamWriter("output.txt", true))
            {
                writer.WriteLineAsync("Elements:" + N + " min: " + min_value + " max: " + max_value + " avg: " + avg);
            }
        }

        static void swap(ref double a, ref double b)
        {
            double temp = a;
            a = b;
            b = temp;
        }

        static double averageArray(double[] array)
        {
            double summ = 0;
            for (int i = 0; i < array.Length; i++)
                summ += array[i];
            double mid = summ / array.Length;
            return mid;
        }

    }

    
}
