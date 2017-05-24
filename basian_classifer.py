from math import e, pi
class NaiveBayes:
    def __init__(self, user_input):
        self.user_input = user_input

    def mssdev(self, the_list, x):

        self.o = pow(sum([pow(i-sum(the_list)/float(len(the_list)), 2) for i in the_list])/float((len(the_list)-1)), 0.5)

        self.u = sum(the_list)/float(len(the_list))
        return (1/(float(pow(2*pi, 0.5)*self.o)))*pow(e, ((-1*(x-self.u)**2)/float(2*pow(self.o, 2))))

    def functional_density(self, o, u, x):
        if o != 0:
            return (1/(float(pow(2*pi, 0.5)*o)))*pow(e, ((-1*(x-u)**2)/float(2*pow(o, 2))))

        else:
            return None

    def prediction(self, ssdevs, mu, user_input, all_models):
        self.total_prob = {}
        for model in all_models:
            self.density = [self.functional_density(ssdevs[model][column+1], mu[model][column+1], value) for column, value in enumerate(user_input)]
            self.multiplyer = 1
            for i in self.density:
                if i != None:
                    self.multiplyer *= i

            self.total_prob[model] = self.multiplyer

        self.fitted_results = {prob:model for model, prob in self.total_prob.items()}
        return self.fitted_results[max(self.fitted_results.keys())]


    def standard_deviation(self, thelst):
        self.average = sum(thelst)/float(len(thelst))
        self.variance = sum([pow(i-self.average, 2) for i in thelst])
        if len(thelst) == 1:

            return pow(self.variance/float(len(thelst)), 0.5)

        else:
            return pow(self.variance/float(len(thelst)-1), 0.5)

    def means(self, thelst):
        return sum(thelst)/float(len(thelst))

    def classifer(self):
        self.f = open('my_data.txt').readlines()

        self.f = [map(int, i.strip('\n').split()) for i in self.f]


        self.totals = {}

        self.models = [i[len(i)-1] for i in self.f]

        for i in self.models:
            self.totals.setdefault(i, {})


        #below, the sum of all values in each column in our data structure

        for i in self.f:
            for b in range(1, len(i[:len(i)])): #used to be :len(i)-1
                self.totals[i[len(i)-1]][b] = 0


        for i in self.f:
            for b in range(1, len(i[:len(i)])):
                self.totals[i[len(i)-1]][b] += i[b-1]



        ######################Below, the list of all the data in the columns
        self.numericValues = {}

        for i in self.models:
            self.numericValues.setdefault(i, {})



        for i in self.f:
            for b in range(1, len(i[:len(i)])): #used to be :len(i)-1
                self.numericValues[i[len(i)-1]][b] = []

        for i in self.f:
            for b in range(1, len(i[:len(i)])):
                self.numericValues[i[len(i)-1]][b].append(i[b-1])


        ##############################################################################################################
        #Below, calculate standard deviation for the data in each column:
        self.ssd = {}

        for i in self.models:
            self.ssd.setdefault(i, {})

        for i in list(set(self.models)):

            for b in range(1, len(self.f[0])):

                self.standard = self.standard_deviation(self.numericValues[i][b])
                self.ssd[i][b] = self.standard

        #print ssd
        #Calculate the means for each column
        self.the_means = {}

        for i in self.models:
            self.the_means.setdefault(i, {})

        for i in list(set(self.models)):
            for b in range(1, len(self.f[0])):
                self.the_means[i][b] = self.means(self.numericValues[i][b])

        #print the_means


        #the_input = [15, 50, 155]

        return self.prediction(self.ssd, self.the_means, self.user_input, list(set(self.models)))
