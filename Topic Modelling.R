data <- read.csv("tweets.csv")

library(tm)
library(ggplot2)
library(dplyr)
library(topicmodels)
library(tidytext)

c <- Corpus(VectorSource(data$text))
c <- tm_map(c, removeWords, stopwords())
inspect(c)

remove_url <- function(x) gsub('http[^[:space:]]*', '', x)
c <- tm_map(c, content_transformer(remove_url))

removeNumPunct <- function(x) gsub('[^[:alpha:][:space:]]*', '', x)
c <- tm_map(c, content_transformer(removeNumPunct))

c <- tm_map(c, content_transformer(tolower))
c <- tm_map(c, removePunctuation)
c <- tm_map(c, removeWords, stopWordList)
c <- tm_map(c, stripWhitespace)
c <- tm_map(c, stemDocument)

dtm <- DocumentTermMatrix(c)
dtm
inspect(dtm[1:10,])


ap_lda <- LDA(dtm, k = 2, control = list(seed = 1234))
ap_lda

ap_topics <- tidy(ap_lda, matrix = "beta")
ap_topics


ap_top_terms <- ap_topics %>%
  group_by(topic) %>%
  top_n(10, beta) %>%
  ungroup() %>%
  arrange(topic, -beta)

ap_top_terms %>%
  mutate(term = reorder(term, beta)) %>%
  ggplot(aes(term, beta, fill = factor(topic))) +
  geom_col(show.legend = FALSE) +
  facet_wrap(~ topic, scales = "free") +
  coord_flip()


