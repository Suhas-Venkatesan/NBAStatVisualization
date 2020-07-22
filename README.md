# Background and Overview
This is an NBA Visualization web app built with Plot.ly and Dash (a framework that uses React.js and Flask), to view complicated NBA statistics in a simple fashion with graphs and charts. You can check out the app at ____________. 

# Play by Play Visualization
* As a huge fan of the NBA as well as data science, I wanted to create an easy to use tool that would allow a user to look up any game from the 1995-96 season and onwards(games before then do not have play by play data on the website). The user can see a play-by-play graph which illustrates the changes in score throughout the game, which are graphed on the y-axis as the score margin. There is a similar tool to this one already available, but its game selecting interface runs on date instead of by team and season, making it extremely inconvenient. In addition, it only contains games from the 2017-18 NBA season and onwards while my tool contains almost every game starting from the 1995-96 season. The progression of the game is detailed by the graph, and the user can quickly see which team was ahead at what point in the game, how frequently the leads were changed, and how close (or lopsided) the game actually was in its entirety. There is also hover enabled so each made shot and made free throw throughout the game can clearly be visible.

* To start, simply select two teams and a season, and the list of available games will appear in the dropdown menu on the right
![playbyplayexample](https://github.com/Suhas-Venkatesan/NBAStatVisualization/blob/master/screenshots/NBAappScreenshot1.PNG)

* Select any of the available games in order to generate a graph like the following for the game between the Washington Wizards and Cleveland Cavaliers on December 17, 2017. 
![playbyplayexample](https://github.com/Suhas-Venkatesan/NBAStatVisualization/blob/master/screenshots/NBAAppScreenshot2.PNG)

* Some features I may be adding in the future are highlight clicking for individual shots (which show a video of the shot, if it is available), and customized game highlight reels that can be created for any game. 

# Player Shot Charts

* In addition, the app generates player shot charts for any player that played in the NBA starting from the 1995-96 season. After selecting the player and the season, as well as the type of season (regular season, playoffs, pre season, or the all star game), the app generates a shot chart showing all of the player's makes and misses during that year and where on the court they are. Makes are marked by a green dot while misses are marked by a red dot. An example is shown below for Stephen Curry in the latest 2019-20 season which he mostly missed due to injury. 
![playbyplayexample](https://github.com/Suhas-Venkatesan/NBAStatVisualization/blob/master/screenshots/nbaappscreenshot3.PNG)

* Some features that could be added in the future are supplementary charts with hexbins for shot locations and a small statistics bar to the left of the chart that shows some relevant stats (without making it look too complicated)


# Data
All data was retrieved from stats.nba.com using endpoints from the nba-api

