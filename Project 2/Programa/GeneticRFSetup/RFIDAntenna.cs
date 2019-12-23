using System;
namespace GeneticRFSetup
{
    public  class RFIDAntenna
    {
        double[] itensConfiguraveis = new double[31];
        double[] itensIdeais = new double[31];

        // inicializa antena com valores ideais
        public RFIDAntenna() 
        {
            itensIdeais = Program.itensIdeais;
        }

        public void setPosition(int i, double value)
        {
            if(Program.cromossomoVerbose)
            {
                Console.WriteLine($"itensConfiguraveis[{i:D2}] = {value:F2}");
            }
            itensConfiguraveis[i] = value;
        }

        public double ReadCommand()
        {
            itensIdeais = Program.itensIdeais;
            double delta = 0;
            for (int i = 0; i < 31; i++)
            {
                delta += Math.Abs(itensIdeais[i] - itensConfiguraveis[i]);
            }

            return delta / 31;  // RSSI
        }
    }
}
