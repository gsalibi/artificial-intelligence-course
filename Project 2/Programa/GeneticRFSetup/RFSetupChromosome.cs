using System;
using GeneticSharp.Domain.Chromosomes;

namespace GeneticRFSetup
{
    public class RFSetupChromosome : ChromosomeBase
    {
        public RFSetupChromosome() : base(31)
        {
            CreateGenes();
        }

        public override IChromosome CreateNew()
        {
            return new RFSetupChromosome();
        }

        //Cria genes de acordo com as regras
        public override Gene GenerateGene(int geneIndex)
        {
            Random randomGenerator = new Random();
            var value = Convert.ToDouble(randomGenerator.Next(0, 100)) / 100;
            return new Gene(value);
        }
    }
}
