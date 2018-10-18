using System;
using System.Security.Cryptography;

namespace SecureRandom
{
    public class SecureRandomNumberProvider
    {
        private readonly RNGCryptoServiceProvider _provider;

        public SecureRandomNumberProvider()
        {
            _provider = new RNGCryptoServiceProvider();
        }

        public sbyte Next()
        {
            sbyte[] randomBytes = new sbyte[1];

            _provider.GetBytes((byte[])(Array)randomBytes);
            sbyte provisionalResult = randomBytes[0];

            return provisionalResult == sbyte.MinValue ? (sbyte)0 : Math.Abs(provisionalResult);
        }

        public sbyte Next(sbyte maximum)
        {
            sbyte upperbound = (sbyte)(sbyte.MaxValue / maximum * maximum);
            sbyte provisionalResult;

            do
            {
                provisionalResult = Next();
            }
            while (provisionalResult >= upperbound);

            return (sbyte)(provisionalResult % maximum);
        }

        public sbyte Next(sbyte minimum, sbyte maximum)
        {
            if (minimum < 0)
            {
                throw new ArgumentException("Arguments must be greater than zero");
            }
            else if (minimum >= maximum)
            {
                throw new ArgumentException("The first argument must be less than the second");
            }

            return (sbyte)(minimum + Next((sbyte)(maximum - minimum)));
        }

        /// <summary>
        /// this is endianness dependent, only works on little endian system
        /// </summary>
        /// <returns></returns>
        public double NextDouble()
        {
            byte[] randomBytes = new byte[8];

            _provider.GetBytes(randomBytes);
            randomBytes[7] = 0b0011_1111;
            randomBytes[6] |= 0b1111_0000;
            return BitConverter.ToDouble(randomBytes) - 1d;
        }
    }
}