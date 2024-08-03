// User Register - Post
{
    "username":"user1",
    "password":"user1"
}


// Collection create - Post
{
    "title": "My Collection",
    "description": "This is my movie collection.",
    "movies": [
        {
            "title": "Movie 1",
            "description": "Description of movie 1",
            "genres": "Action,Adventure",
            "uuid": "123e4567-e89b-12d3-a456-426614174000"
        },
        {
            "title": "Movie 2",
            "description": "Description of movie 2",
            "genres": "Drama",
            "uuid": "123e4567-e89b-12d3-a456-426614174001"
        }
    ]
}


// Collection Update - Put
{
  "title": "Updated Collection Title",
  "description": "Updated description of the collection.",
  "movies": [
    {
      "title": "Updated Movie 1",
      "description": "Updated description of movie 1",
      "genres": "Action,Adventure",
      "uuid": "123e4567-e89b-12d3-a456-426614174000"
    },
    {
      "title": "Updated Movie 2",
      "description": "Updated description of movie 2",
      "genres": "Drama",
      "uuid": "123e4567-e89b-12d3-a456-426614174001"
    }
  ]
}
