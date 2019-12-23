using System;
using System.Diagnostics;
using GeneticSharp.Domain;
using GeneticSharp.Domain.Populations;
using GeneticSharp.Domain.Selections;
using GeneticSharp.Domain.Crossovers;
using GeneticSharp.Domain.Mutations;
using GeneticSharp.Domain.Terminations;

namespace GeneticRFSetup
{
    class Program
    {
        public static double[] itensIdeais = new double[31];
        public static GeneticAlgorithm ga;
        public static int nextGeneration = 2;
        public static bool cromossomoVerbose;
        public static bool genesVerbose;

        static void Main(string[] args)
        {
            Random randomGenerator = new Random();
            // inicializa antena com valores randômicos ideais 
            for (int i = 0; i < 31; i++)
            {
                itensIdeais[i] = Convert.ToDouble(randomGenerator.Next(0, 100)) / 100;
            }

            Run();
        }

        private static void Run()
        {
            ISelection selection;
            ICrossover crossover;
            IMutation mutation;
            var fitness = new RFFitness();
            var chromosome = new RFSetupChromosome();

            // entrada do usuário
            Console.Write("Tamanho máximo da população: ");
            var nCromossomos = Convert.ToInt32(Console.ReadLine());
            Console.Write("\nNúmero de gerações (0 para sem limites): ");
            var nGeracoes = Convert.ToInt32(Console.ReadLine());
            Console.Write("\nTécnica de seleção:\n1 - Elite Selection\n2 - Roulette Wheel Selection\n3 - Tournament Selection\n");
            var tipo = Convert.ToInt32(Console.ReadLine());
            switch (tipo)
            {
                case 1:
                    selection = new EliteSelection();
                    break;
                case 2:
                    selection = new RouletteWheelSelection();
                    break;
                default:
                    selection = new TournamentSelection();
                    break;
            }
            Console.Write("\nTécnica de crossover:\n1 - Uniform Crossover\n2 - Three Parent Crossover\n3 - One Point Crossover\n");
            tipo = Convert.ToInt32(Console.ReadLine());
            switch (tipo)
            {
                case 1:
                    crossover = new UniformCrossover(); // Default Mix probability: 50%
                    break;
                case 2:
                    crossover = new ThreeParentCrossover();
                    break;
                default:
                    crossover = new OnePointCrossover();
                    break;
            }
            Console.Write("\nProbabilidade de crossover (entre 0 e 100): ");
            var probCrossover = float.Parse(Console.ReadLine()) / 100;
            Console.Write("\nTécnica de mutação:\n1 - Uniform Mutation\n2 - Reverse Sequence Mutation\n3 - Twors Mutation\n");
            tipo = Convert.ToInt32(Console.ReadLine());
            switch (tipo)
            {
                case 1:
                    mutation = new UniformMutation(true); // todos os genes sao mutaveis
                    break;
                case 2:
                    mutation = new ReverseSequenceMutation();
                    break;
                default:
                    mutation = new TworsMutation();
                    break;
            }
            Console.Write("\nProbabilidade de mutação (entre 0 e 100): ");
            var probMutation = float.Parse(Console.ReadLine()) / 100;
            Console.Write("\nImprimir todos os genes dos melhores cromossosmos:\n1 - Sim\n2 - Não\n");
            var imprimirGenes = Convert.ToInt32(Console.ReadLine());
            genesVerbose = imprimirGenes == 1 ? true : false;
            Console.Write("\nImprimir todos os cromossomos com os genes:\n1 - Sim\n2 - Não\n");
            var imprimirCromossomos = Convert.ToInt32(Console.ReadLine());
            cromossomoVerbose = imprimirCromossomos == 1 ? true : false;

            // seta algoritmo com dados fornecidos
            var population = new Population(nCromossomos, nCromossomos, chromosome);
            ga = new GeneticAlgorithm(population, fitness, selection, crossover, mutation);
            ga.CrossoverProbability = probCrossover;
            ga.MutationProbability = probMutation;
            if (nGeracoes == 0)
            {
                ga.Termination = new FitnessThresholdTermination(1);
            }
            else
            {
                ga.Termination = new GenerationNumberTermination(nGeracoes);
            }

            // inicializa contador de tempo
            var timer = new Stopwatch();
            timer.Start(); 

            // inicia algoritmo
            ga.Start();

            // imprime fitness do melhor resultado
            Console.WriteLine($"\nBest of all solutions found has {ga.BestChromosome.Fitness} fitness.");
           
            // imprime comparativo do melhor resulatdo alcançado com o ideal
            Console.WriteLine($"BEST | IDEAL");
            for (int i = 0; i < 31; i++)
            {
                Console.WriteLine($"{ga.BestChromosome.GetGene(i).Value:F2} | {itensIdeais[i]:F2}");
            }

            // termina contador de tempo e imprime
            timer.Stop();
            TimeSpan ts = timer.Elapsed;
            Console.WriteLine($"O PROGRAMA RODOU EM {ts.Hours}h:{ts.Minutes}min:{ts.Seconds}s:{ts.Milliseconds}ms");
        }
    }
}
