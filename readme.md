# Project Description

This was an analysis of a social network graph, of real and fake news tweeters,
performed for my *Complex Network Dynamics* CS course.

The concept hypothesis and results, are being described in detail in 
[Clustering_and_Misinformation_Report.pdf](Clustering_and_Misinformation_Report.pdf) 
as well as presented in 
[Clustering_and_Misinformation_Presentation.pdf](Clustering_and_Misinformation_Presentation.pdf)
.

---

### Data source

- https://github.com/KaiDMML/FakeNewsNet/tree/old-version

---

### Environment

- Python 3.8 was used

---

### Execution instructions

- Run the 'main.py' script.

---

### Execution output

All outputs for the four first 4 tasks are on the terminal. 

###### Example of terminal output

	Task 1:
		 7316 total users posted real news on BuzzFeed
		 7406 total users posted fake news on BuzzFeed
		 535 total users posted both real and fake news on BuzzFeed
		 4437 total users posted real news on PolitiFact
		 18862 total users posted fake news on PolitiFact
		 566 total users posted both real and fake news on PolitiFact
	
	Task 2:
		Average tweet rate for BuzzFeed real news: 1.41
		Average tweet rate for BuzzFeed fake news: 1.37
		Average re-tweet rate for BuzzFeed real news: 1.1
		Average re-tweet rate for BuzzFeed fake news: 1.11
		Average tweet rate for PolitiFact real news: 1.51
		Average tweet rate for PolitiFact fake news: 1.27
		Average re-tweet rate for PolitiFact real news: 1.09
		Average re-tweet rate for PolitiFact fake news: 1.15
	
	Task 3:
		Average BuzzFeed users following of users that posted real news: 40.88 [group max: 3898 ]
		Average BuzzFeed users followers of users that posted real news: 40.56 [group max: 1269 ]
		Average BuzzFeed users following of users that posted fake news: 41.92 [group max: 4021 ]
		Average BuzzFeed users followers of users that posted fake news: 42.55 [group max: 2004 ]
		Average PolitiFact users following of users that posted real news: 25.26 [group max: 5156 ]
		Average PolitiFact users followers of users that posted real news: 24.76 [group max: 1218 ]
		Average PolitiFact users following of users that posted fake news: 23.62 [group max: 5850 ]
		Average PolitiFact users followers of users that posted fake news: 23.8 [group max: 1470 ]
	
	Task 4:
		Average of connections from real news posters to real news posters on BuzzFeed : 19.07
		Average of connections from real news posters to fake news posters on BuzzFeed : 20.34
		Average of connections from fake news posters to real news posters on BuzzFeed : 19.64
		Average of connections from fake news posters to fake news posters on BuzzFeed : 20.76
		Average of connections from real news posters to real news posters on PolitiFact : 4.79
		Average of connections from real news posters to fake news posters on PolitiFact : 19.79
		Average of connections from fake news posters to real news posters on PolitiFact : 4.53
		Average of connections from fake news posters to fake news posters on PolitiFact : 18.44
	
	Task 5:
		Export DONE

--- 

### Output files

The following files are being created by the script and/or being provided:
- **realreal.csv**, **realfake.csv**, **fakereal.csv**,
**fakefake.csv** are produced for both networks from the script, for Gephi 
analysis.
- **Real.csv**, **Fake.csv** for each network, are created by concatenating 
realreal + realfake ect, files for each network.
- Gephi analysis output is saved and stored on **gephi_analysis_results** 
directory.
