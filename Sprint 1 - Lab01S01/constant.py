URL = 'https://api.github.com/graphql'
TOKEN = 'INSERT YOUR TOKEN HERE'
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'bearer {TOKEN}'
}
QUERY = """
{
  search(query: "stars:>100 language:java", type: REPOSITORY, first:5{AFTER}) {
    pageInfo {
      startCursor
      endCursor
      hasNextPage
      hasPreviousPage
    }
    nodes {
      ... on Repository {
        nameWithOwner
        url
        createdAt
        primaryLanguage {
          name
        }
        languages(orderBy: {field: SIZE, direction: DESC}, first: 1) {
          totalSize
          totalCount
          edges {
            size
            node {
              name
            }
          }
        }
        stargazers {
          totalCount
        }
        releases {
          totalCount
        }
      }
    }
  }
}
"""
PATH_CSV = '/output_github.csv'
