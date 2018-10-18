using System;
using SecureRandom;

namespace SecureRandomTests
{
    public class SecureRandomTests
    {
        public static void Main()
        {
            SecureRandomNumberProvider _provider = new SecureRandomNumberProvider();

            int[] results = new int[128];
            int randomResult;
            for (int i = 0; i < 10000000; i++)
            {
                randomResult = _provider.Next();
                results[randomResult] += 1;
            }

            for (int i = 0; i < 128; i++)
                Console.WriteLine(i.ToString() + ": " + results[i].ToString());

            Console.WriteLine();

            results = new int[10];

            for (int i = 0; i < 10000000; i++)
            {
                randomResult = _provider.Next(10);
                results[randomResult] += 1;
            }

            for (int i = 0; i < 10; i++)
                Console.WriteLine(i.ToString() + ": " + results[i].ToString());

            Console.WriteLine();

            results = new int[20];

            for (int i = 0; i < 10000000; i++)
            {
                randomResult = _provider.Next(10, 20);
                results[randomResult] += 1;
            }

            for (int i = 10; i < 20; i++)
                Console.WriteLine(i.ToString() + ": " + results[i].ToString());

            Console.WriteLine();

            results = new int[100];
            double randomDoubleResult;

            for (int i = 0; i < 10000000; i++)
            {
                randomDoubleResult = _provider.NextDouble();
                results[(int)(randomDoubleResult * 100)] += 1;
            }

            for (int i = 0; i < 100; i++)
                Console.WriteLine(i.ToString() + ": " + results[i].ToString());

            Console.ReadLine();
        }
    }
}