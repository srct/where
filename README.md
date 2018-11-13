# where

Map out points of interest at Mason, like water fountains, bathrooms, and study spots.

Ideas/Planning: [https://go.gmu.edu/where-ideas](https://go.gmu.edu/where-ideas)

For updates, join #where on Slack.

# Running

First run `npm install` or `yarn`. Then run `npm run build` to build then project, and then `npm run start`. You should then be able to view the site [in your browser](http://localhost:3000/)

Alternatively, you can use Docker Compose by running `docker-compose up`. You can build and run the Docker container on it's own by executing the following

```
docker build -t where .
docker run -p 3000:3000 where
```
