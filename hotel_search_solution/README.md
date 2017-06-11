# Hotel Search API Solution

Kevan Swanberg's solution for the hotel search problem.

# Running the server

`python -m hotel_search_solution.resultapi`

starts the server on port 8000, only responds to `/hotels/search`


# Architecture

I decided to use python + tornado. I noticed in the test that it was expecting a sub 3 second response and it would need to
make 5 http requests that all were resolving in 2 seconds. I needed to do asyncrhonous IO so that the requests could all happen at once.
I considered node, using python3 async. Decided that since this environment was already set and ready to go with tornado using that
would be the path of least resistance.

# Solution

I use tornado's AsyncHttpClient to create the requests and store a list of futures to wait for the responses to come in.
When they are all in each response is parsed and it's hotels added to a list of 2-tuples.
The first element of the tuple is the hotel's ecstasy and the second is the hotel data.
To use python's heapq.merge they need to be in reverse order so the hotel's with the smallest ecstasy come first.
Then I merge all the lists of tuples. The result is a list of tuples with smallest ecstasy first.
I reverse that list and convert it from a list of tuples to a list with just the hotel data and write the response.
