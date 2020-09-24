Title: How to use both camelCase and snake_case in frontend and backend
Description: How to use camel_case in your Python and camelCase in your JavaScript at the same time.
Slug: camel-and-snake-case
Date: 2020-09-24 12:00
Category: Django

Python uses `snake_case` variable naming while JavaScript favours `camelCase`. 
When you're buiding an web API with Django then you'll be using both langauges together. How do you keep your styles consistent? You _could_ just use one style for both your frontend and backend, but it looks ugly. Perhaps this is not the biggest problem in your life right now, but it's a nice one to solve and it's easy to fix.

In this post I'll show you can use snake case on the backend and camel case on the frontend, with the help of the the `camelize` and `snakeize` JS libraries.

### The problem: out of place naming styles

Let's say you've got some Django code that presents an API for a `Person` model:

```python
# Inside your Django app.
# The data model
class Person(models.Model):
    full_name = models.CharField(max_length=64)
    biggest_problem = models.CharField(max_length=128)

# The serializer
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["full_name", "biggest_problem"]

# The API view
class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
```

And you've also got some JavaScript code that talks to this view:

```javascript
// Inside your frontend JavaScript codebase.
const createPerson = (personData) => {
    requestData = {
      method: 'POST',
      body: JSON.stringify(personData),
      // etc.
    }
    const response = await fetch('/api/person/', requestData)
    return await resp.json()
}
```

The problem occurs when you try to use the data fetched from the backend and it is using the wrong variable naming style:

```javascript
// Inside your frontend JavaScript codebase.
const personData = {
    full_name: 'Matt Segal',
    biggest_problem: 'My pants are too red',
}
const person = createPerson(personData).then(console.log)
// {
//   full_name: 'Matt Segal',
//   biggest_problem: 'My pants are too red',
// }
```

This usage of snake case in JavaScript is a little yucky and it's a quick fix.

### The solution: install more JavaScript libraries

Hint: the solution is always to add more dependencies.

To fix this we'll install [snakeize](https://www.npmjs.com/package/snakeize) and [camelize](https://www.npmjs.com/package/camelize) using npm or yarn:

```bash
yarn add snakeize camelize
```

Then you just need to include it in your frontend's API functions:

```javascript
// Inside your frontend JavaScript codebase.
import camelize from 'camelize'
import snakeize from 'snakeize'

const createPerson = (personData) => {
    requestData = {
      method: 'POST',
      body: JSON.stringify(snakeize(personData)),
      // etc.
    }
    const response = await fetch('/api/person/', requestData)
    const responseData = await resp.json()
    return camelize(responseData)
}
```

Now we can use `camelCase` in the frontend and it will automatically be transformed to `snake_case` before it gets sent to the backend:

```javascript
// Inside your frontend JavaScript codebase.
const personData = {
    fullName: 'Matt Segal',
    biggestProblem: 'I ate too much fish',
}
const person = createPerson(personData).then(console.log)
// {
//   fullName: 'Matt Segal',
//   biggestProblem: 'I ate too much fish',
// }
```

That's it! Hope this helps your eyes a little.
