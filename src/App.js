import "./App.css";
import { TextField } from "@mui/material";

import Button from "@mui/material/Button";
import { useState, useEffect, Fragment } from "react";
import wnn from "words-n-numbers";

// Files to inverted index and other needed files
import { indexer } from "./static/indexes/indexer";
import { tweetData } from "./static/indexes/tweet_doc";
import { blogData } from "./static/indexes/blog_doc";
import { obsidianData } from "./static/indexes/obsidian_doc";
import { emailData } from "./static/indexes/email_doc";

const sumValues = (obj) => Object.values(obj).reduce((a, b) => a + b);

function flatten(arr) {
  return arr.reduce(function (flat, toFlatten) {
    return flat.concat(
      Array.isArray(toFlatten) ? flatten(toFlatten) : toFlatten
    );
  }, []);
}

function App() {
  const [searchInput, setSearchInput] = useState("");
  const [returnedDocs, setReturnedDocs] = useState([]);
  const [searchTime, setSearchTime] = useState("");
  const [selectedDoc, setSelectedDoc] = useState("");
  const [selectedDocType, setSelectedDocType] = useState("");
  const numDocs =
    tweetData.length + blogData.length + emailData.length + obsidianData.length;

  const clearDocs = () => {
    setSelectedDoc("");
    setSelectedDocType("");
  };

  useEffect(() => {
    if (!searchInput) {
      setReturnedDocs([]);
      return;
    }

    const starttTime = performance.now();

    const tokenizedInput = wnn.extract(searchInput);
    console.log(tokenizedInput);

    let docList = [];

    for (const token of tokenizedInput) {
      if (token in indexer) {
        docList.push([indexer[token]]);
      }
    }

    console.log(docList);

    if (docList.length === 0) {
      setReturnedDocs([]);
      return;
    }

    console.log(docList);
    // Converts list to set to remove dupes
    const flattenedDocs = [...new Set(flatten(docList))];

    console.log(flattenedDocs);

    // Change this to be an AND rather than an OR
    const docs = [];
    const docMap = {};
    if (flattenedDocs) {
      for (let i = 0; i < flattenedDocs.length; i++) {
        const docId = flattenedDocs[i];
        // console.log(docId);
        const type = docId.slice(0, 2);
        // console.log(type);
        const num = docId.slice(2);
        let doc;
        if (type === "tw") {
          doc = tweetData[num];
        } else if (type === "em") {
          doc = emailData[num];
        } else if (type === "ob") {
          doc = obsidianData[num];
        } else if (type === "ww") {
          doc = blogData[num];
        }

        docs.push(doc);
        docMap[doc.id] = doc;
      }

      const scoredDocs = {};

      for (const doc of docs) {
        console.log(doc);
        let score = 0;
        for (const token of tokenizedInput) {
          let currScore = 0;
          console.log(token);
          if (token in doc.tokens) {
            currScore =
              (doc.tokens[token] / sumValues(doc.tokens)) *
              Math.log(docs.length / Object.keys(doc.tokens).length);
          }
          score += currScore;
        }
        scoredDocs[doc.id] = score;
      }
      let sortedDocs = Object.entries(scoredDocs).sort((a, b) => b[1] - a[1]);

      const newDocs = [];
      sortedDocs.forEach((doc) => {
        newDocs.push(docMap[doc[0]]);
      });

      setReturnedDocs(newDocs);
      const endTime = performance.now();
      setSearchTime((endTime - starttTime).toFixed(3));
    }
  }, [searchInput]);

  const wordMap = {
    ww: "blog",
    tw: "twitter",
    ob: "obsidian",
    em: "newsletter",
  };

  return (
    <div className="container">
      <div className="App">
        <TextField
          autoFocus
          fullWidth
          onChange={(e) => setSearchInput(e.target.value)}
          value={searchInput}
          style={{ backgroundColor: "white", borderRadius: "5px" }}
          placeholder={"Type to search through " + numDocs + " docs"}
        />

        {!searchInput ? (
          <div className="welcome-container">
            <p>
              Hi friend! You've found a search engine into my second brain!
              Stick around for a while, maybe you'll find something of interest.
            </p>
            <b>Unsure what to search? Try:</b>
            <div>
              <button className="tags" onClick={() => setSearchInput("life")}>
                life
              </button>
              <button className="tags" onClick={() => setSearchInput("tools")}>
                tools
              </button>
              <button
                className="tags"
                onClick={() => setSearchInput("startup")}
              >
                startup
              </button>
              <button className="tags" onClick={() => setSearchInput("design")}>
                design
              </button>
            </div>
            <h2>What is this?</h2>
            I'm calling this project Watcher (which is a bit dystopian I know)
            but it was built for a class called Collective Cognition
            (specifically around transactive memory systems). Heavily inspired
            by{" "}
            <a
              href="https://github.com/thesephist/monocle"
              target="_blank"
              rel="noreferrer"
            >
              Linus Lee's Monocole
            </a>{" "}
            project and{" "}
            <a
              href="https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/"
              target="_blank"
              rel="noreferrer"
            >
              Bret Victor's Memex
            </a>
            . Want to chat more?{" "}
            <a
              href="https://twitter.com/zhaovan8"
              target="_blank"
              rel="noreferrer"
            >
              DM me!
            </a>
          </div>
        ) : (
          <Fragment />
        )}

        {returnedDocs.length === 0 && searchInput ? (
          <p style={{ textAlign: "left" }}>
            There's nothing in my brain about this :/
          </p>
        ) : (
          <Fragment />
        )}
        {returnedDocs.length > 0 ? (
          <p className="timer">
            Found {returnedDocs.length} docs ({searchTime} ms)
          </p>
        ) : (
          <Fragment />
        )}

        {/* Section that renders documents */}
        {returnedDocs.length > 0 ? (
          returnedDocs.map((doc, i) => {
            return (
              <div
                key={i}
                className="result"
                onClick={() => {
                  setSelectedDocType(doc.id.slice(0, 2));
                  setSelectedDoc(doc);
                }}
              >
                <span className="result-tag">
                  {wordMap[doc.id.slice(0, 2)]}
                </span>
                <p style={{ marginLeft: "4%" }}></p>
                <p style={{ margin: "0%" }}>
                  {" "}
                  <span style={{ fontWeight: 600 }}>
                    {doc.title ? doc.title + ": " : ""}
                  </span>
                  <span className="content">
                    {doc.content.substring(0, 144)}
                  </span>
                </p>
              </div>
            );
          })
        ) : (
          <Fragment />
        )}
        {selectedDoc ? (
          <div className="selected-doc">
            <div className="selected-doc-header">
              {selectedDoc.href ? (
                <a
                  href={selectedDoc.href}
                  target="_blank"
                  rel="noreferrer"
                  className="header-item"
                >
                  <Button variant="outlined">Link</Button>
                </a>
              ) : (
                <Fragment />
              )}
              <Button
                variant="outlined"
                onClick={() => clearDocs()}
                className="header-item"
              >
                Close
              </Button>
            </div>
            <div className="selected-doc-content">
              {selectedDoc.title ? <h1>{selectedDoc.title}</h1> : <Fragment />}
              <p className="doc-content">
                {selectedDocType !== "tw"
                  ? selectedDoc.content
                  : selectedDoc.content}
              </p>
            </div>
          </div>
        ) : (
          <Fragment />
        )}
      </div>
    </div>
  );
}

export default App;
