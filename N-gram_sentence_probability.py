#!/usr/bin/env python3

# N-gram probability estimation
# Yawen Zhang
# March 2nd, 2017

import math
import re
from sys import argv
from collections import defaultdict
    
class NgramCount:
    """
    Class to count N-gram
    """
    # get N-gram counts
    def GetUnigramAndBigramCounts(self, n, data):
        ngram = {}
        for x in data:
            x = x.split(" ")
            for i in range(len(x)-n+1):
                grams = ' '.join(x[i:i+n])
                ngram.setdefault(grams, 0)
                ngram[grams] += 1
        return ngram

class NgramProb:
    """
    Class to calcualte N-gram probability
    """
    def GetUnigramProbabilities(self, unigram_data):
        # count the total instances of tokens, get rid of start and ending tokens
        total_count = sum(unigram_data.values()) - unigram_data["<s>"] - unigram_data["</s>"]
        # define the unigram prob.
        unigram_prob = {}
        for key, value in unigram_data.items():
            if key not in ["<s>", "</s>"]:
            	unigram_prob[key] = math.log10(value/total_count)
        return unigram_prob

    def GetBigramProbabilities(self, unigram_data, bigram_data):
        # define the bigram prob.
        bigram_prob = {}
        # get bigram probability        
        for key, value in bigram_data.items():
        	key_unigram = key.split(" ")[0]
        	bigram_prob[key] = math.log10(value/unigram_data[key_unigram])
        return bigram_prob

    def GetSmoothedProbabilities(self, unigram_data, bigram_data):
        # define k
        k = 0.0001

        # define the smoothed bigram prob.
        smoothed_bigram_prob = {}
        # get smoothed bigram probability
        for key, value in bigram_data.items():
            key_unigram = key.split(" ")[0]
            smoothed_bigram_prob[key] = math.log10((value + k)/(unigram_data[key_unigram] + k*(len(unigram_data)-2)))
        
        return smoothed_bigram_prob

class NgramSentenceProb:
    """
    Class to estimate sentence N-gram probability
    """
    def GetUnigramSentenceProbability(self, sentence, unigram_prob):
        sentence = sentence.replace("\n", "")
        tokens = sentence.split(" ")

        unigram_sentence_prob = 0
        for x in tokens:
            if x in unigram_prob.keys():
                unigram_sentence_prob += unigram_prob[x]
            else:
                unigram_sentence_prob = 0
                break            
        return unigram_sentence_prob

    def GetBigramSentenceProbability(self, sentence, unigram_prob, bigram_prob):
        # add start and ending tokens to sentence
        sentence = "<s> " + sentence.replace("\n", " </s>")
        tokens = sentence.split(" ")
       
        # get bigram from sentence
        sentence_bigram = []
        for i in range(len(tokens)-1):
            g = ' '.join(tokens[i:i+2])
            sentence_bigram.append(g)
        
        # estimate sentence bigram probability using chain rule
        bigram_sentence_prob = 0
        for j in sentence_bigram:
            if j in bigram_prob.keys():
            	bigram_sentence_prob += bigram_prob[j]
            else:
                # if not in the bigram prob. model, set prob. to zero
                bigram_sentence_prob = 0
                break
        return bigram_sentence_prob

    def GetSmoothedSentenceProbability(self, sentence, unigram_data, unigram_prob, smoothed_bigram_prob):
        k = 0.0001
        # add start and ending tokens to sentence
        sentence = "<s> " + sentence.replace("\n", " </s>")
        tokens = sentence.split(" ")

        # get bigram from sentence
        smoothed_sentence_bigram = []
        for i in range(len(tokens)-1):
            g = ' '.join(tokens[i:i+2])
            smoothed_sentence_bigram.append(g)
        
        # estimate sentence smoothed bigram probability using chain rule
        smoothed_bigram_sentence_prob = 0
        for j in smoothed_sentence_bigram:
            if j in smoothed_bigram_prob.keys():
                smoothed_bigram_sentence_prob += smoothed_bigram_prob[j]
            else:
                # if not in the bigram prob. model, calculate the smoothed bigram prob. 
                j_unigram = j.split(" ")[0]
                smoothed_bigram_sentence_prob += math.log10(k/(unigram_data[j_unigram] + k*(len(unigram_data)-2)))
        return smoothed_bigram_sentence_prob

if __name__ == "__main__":

    # read the training data
    train_file = argv[1]
    # open the training data
    with open(train_file, 'r') as f:
    	train_data = f.readlines()
    # change all to lowercase
    train_data = [x.lower() for x in train_data]
    # add start and ending token for each sentence
    train_data = ["<s> " + x.replace("\n", " </s>") for x in train_data]

    # count N-gram   
    ngram_count = NgramCount()
    unigram_count = ngram_count.GetUnigramAndBigramCounts(1, train_data)   
    # print("unigram count:", len(unigram_count))
    bigram_count = ngram_count.GetUnigramAndBigramCounts(2, train_data)
    # print("bigram count:", len(bigram_count))

    # build N-gram model
    ngram_prob = NgramProb()
    unigram_prob = ngram_prob.GetUnigramProbabilities(unigram_count)
    bigram_prob = ngram_prob.GetBigramProbabilities(unigram_count, bigram_count)
    smoothed_bigram_prob = ngram_prob.GetSmoothedProbabilities(unigram_count, bigram_count)

    # read the testing data
    test_file = argv[2]
    # open the testing data
    with open(test_file, 'r') as f:
    	test_data = f.readlines()

    # estimate sentence N-gram probability for test data
    for sentence in test_data:
        print("S = ", sentence)
        
        # change to lowercase sentence
        sentence = sentence.lower()        

        ngram_sentence_prob = NgramSentenceProb()
        unigram_sentence_prob = ngram_sentence_prob.GetUnigramSentenceProbability(sentence, unigram_prob)
        if unigram_sentence_prob != 0:
            print("Unigrams: logprob(S) = ", round(unigram_sentence_prob, 4))
        else:
            # if prob equals to 0
            print("Unigrams: logprob(S) = undfined")
        bigram_sentence_prob = ngram_sentence_prob.GetBigramSentenceProbability(sentence, unigram_prob, bigram_prob)
        if bigram_sentence_prob != 0:
            print("Bigrams: logprob(S) = ", round(bigram_sentence_prob, 4))
        else:
            # if prob equals to 0
            print("Bigrams: logprob(S) = undefined")
        smoothed_bigram_sentence_prob = ngram_sentence_prob.GetSmoothedSentenceProbability(sentence, unigram_count, unigram_prob, smoothed_bigram_prob)
        if smoothed_bigram_sentence_prob != 0:
            print("Smoothed Bigrams: logprob(S) = ", round(smoothed_bigram_sentence_prob, 4))
        else:
            # if prob equals to 0
            print("Smoothed Bigrams: logprob(S) = undefined")
        print("\n")  



