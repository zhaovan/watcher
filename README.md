# Watcher: My best friend for finding local information

![](/public/display.png)

This is a project for CLPS1220B: Collective Cognition. I was curious about the ways that we could use the internet as a transactive memory system, specifically in relation to Vannevar Bush's [Memex](theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881) of having a read version where we could look through databases of information that applies to us instantly. Specifically, this piece from the [Scientific American](https://www.scientificamerican.com/article/the-internet-has-become-the-external-hard-drive-for-our-memories/) is what peaked this curiosity during the class.

Heavily inspired by Linus Lee's [Monocle Project](https://github.com/thesephist/monocle) and some other previous examples of memex's

## Applications to Collective Cognition

There's two main applications. The first is the fact that one of the views is that individuals who have effective memory recall are able to contribute more successfully to group projects. This can be seen in the fact that in meetings or other discussion based activities, individuals with notes / those who come prepared and have thought about what they're saying are more active contributors. Besides the direct idea into transactive memory systems, it also creates faster read access into someone else's brain. One of the fundamental problems in collective cognition is around cooperation and collaboration problems. This is even seen in crypto and other governance related issues but having quick speed into other people's notes/ideas/brain space can serve as a first step in solving this issue

## Details and Implementation

![](/public/diagram.png)

This is a static web app built with create-react-app and hosts a python library for creating an index of notes.

## Data Sources

Currently this supports four main data sources: obsidian, twitter, blogs, and my email newsletter. Future implementations would look at Readwise, Pocket, and other web based sources but was unable to get to this due to limitations of time.

```typescript
type Doc = {
  // identifier for blocks
  id: string;
  // A map of each token in the document to the number of times it appears
  // in the document.
  tokens: Map<string, number>;
  // The document's text content
  content: string;
  // Optionally, the doc's title
  title?: string;
  // Optionally a link to this document on the web if it exists
  href?: string;
};
```

### Tokenizing

The algorithm uses the nltk package form python for tokenizing which removes most common stop words and punctuation (which is helpful when we're searching later since rarely am I searching for a specific punctuation). From here, this produces the doc with doc tokens (as seen above).

### Index

After all the docs have been generated, we now have lists of docs for each different type of data source that we have. From here, we iterate through each document to create an [inverted index](https://en.wikipedia.org/wiki/Inverted_index). This massive JSON is then passed to the frontend for querying.

### Frontend

Built on top of material-ui (one of my favorite libraries), some css love, and a lot of tears. We tokenize the query and search for the union (not the intersection, mostly because I couldn't get it to work). From here, we run the standard [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) algorithm on the docuemnts to get our search results.
