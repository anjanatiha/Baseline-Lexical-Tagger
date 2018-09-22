## Baseline Lexical Tagger
### Description:
1.	Builds a baseline statistical tagger by using the assignment#2's hash of hashes.
2.	Train baseline lexicalized statistical tagger on the entire BROWN corpus.
3.	Uses the baseline lexicalized statistical tagger to tag all the words in the SnapshotBROWN.pos.all.txt file.
4.	Evaluates and reports the performance of this baseline tagger on the Snapshot file.
5.	Adds rules for unknown word tagging.
6.	Tests on new text collected from article.

### Description (Detailed):
1.	Maps each parse tree in the BROWN.pos.all file into one-line sentences.
2.	Each sentence spans a single line in the output file.
3.	Generates the hash of hashes from the clean file BROWN-clean.pos.txt in word:pos:freq format.
4.	Takes the most frequent tag and use it to tag the words in all the sentences from the SnapshotBROWN-clean.pos.txt file.
5.	Report the performance (Accuracy, error, percentile not present in tag set) of this tagger.

#### Tools Requirement: Anaconda, Python 

Current Version  : v1.0.2.1

Last Update      : 02.28.2018 (Time : 06:22am)

