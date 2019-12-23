using System;
using GeneticSharp.Domain.Chromosomes;
using GeneticSharp.Domain.Fitnesses;

namespace GeneticRFSetup
{
    internal class RFFitness : IFitness
    {
        public static int cromossomoAtual = 0;

        public double Evaluate(IChromosome chromosome)
        {
            var genes = chromosome.GetGenes();
            var antenna = new RFIDAntenna();

            if (Program.ga.GenerationsNumber == Program.nextGeneration)
            {
                cromossomoAtual = 0;
                Program.nextGeneration++;
                Console.WriteLine($"Best solution of generation {Program.ga.GenerationsNumber - 1:D6} found has {Program.ga.BestChromosome.Fitness:F15} fitness.");
                if (Program.genesVerbose)
                {
                    Console.WriteLine($"BEST | IDEAL");
                    for (int i = 0; i < 31; i++)
                    {
                        Console.WriteLine($"{Program.ga.BestChromosome.GetGene(i).Value:F2} | {Program.itensIdeais[i]:F2}");
                    }
                }
            } 

            cromossomoAtual++;
            if (Program.cromossomoVerbose)
            {
                Console.WriteLine($"\n\nGERACAO: {Program.ga.GenerationsNumber} / Cromossomo: {cromossomoAtual}");
            }

            for (int i = 0; i < 31; i++)
            {
                antenna.setPosition(i, Convert.ToDouble(genes[i].Value));
            }

            return 1 - antenna.ReadCommand();  // fitness
        }

    }
}