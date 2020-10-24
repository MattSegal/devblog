Title: How to setup Django with React
Description: An opinionated guide on adding React to a Django project
Slug: django-react
Date: 2020-10-24 12:00
Category: Django

It's not too hard to get started with either Django or React. Both have great documentation and there are lots of tutorials online. 
The tricky part is getting them to work together. Many people start with a Django project and then decide that they want to "add React" to it.
How do you do that though? Popular React scaffolding tools like [Create React App](https://github.com/facebook/create-react-app) don't offer you a clear way to integrate with Django, leaving you to figure it out yourself. Even worse, there isn't just one way to set up a Django/React project. There are dozens of [possible methods](https://mattsegal.dev/django-spa-infrastructure.html), each with different pros and cons. Every time I create a new project using these tools I find the options overwhelming.

I think that most people should start with a setup that is as close to vanilla Django as possible: you take your existing Django app and sprinkle a little React on it to make the frontend more dynamic and interactive. For most cases, creating a completely seperate "single page app" frontend creates a lot of complexity and challenges without providing very much extra value for you or your users.

In this series of posts I will present an opinionated guide on how to setup and deploy a Django/React webapp. The focus will be on keeping things simple, incremental and understanding each step. I want you to be in a position to debug any problems yourself. At the end of each post, you should have a working project that you can use.

I'm going to assume that you know:

- the [basics of web development](https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web) (HTML, CSS, JavaScript)
- the [basics of Django](https://docs.djangoproject.com/en/3.1/intro/tutorial01/) (views, templates, static files)
- the [basics of React](https://reactjs.org/tutorial/tutorial.html) (components, props, rendering)

I'm **not** going to assume that you know anything about Webpack, Babel, or any other JavaScript toolchain insanity.

## Example project

The example code for this guide is hosted on [this GitHub repo](https://github.com/MattSegal/django-react-guide). The code for each section is available as a Git branch:

-  [Starting point](https://github.com/MattSegal/django-react-guide/tree/part-1-initial-django)
-  [Adding Webpack](https://github.com/MattSegal/django-react-guide/tree/part-2-add-webpack)
-  [Adding Babel and React](https://github.com/MattSegal/django-react-guide/tree/part-3-add-babel-and-react)

Before you start the rest of the guide, I recommend setting up the example project by cloning the repo and following the instructions in the [README](https://github.com/MattSegal/django-react-guide/blob/part-1-initial-django/README.md):

```bash
git clone https://github.com/MattSegal/django-react-guide.git
```

<div class="loom-embed"><iframe src="https://www.loom.com/embed/d238b8eb58dd44c89af7a4e3dd0c42a1" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>


## Django and static files

Before we dig into React, Babel and Webpack, I want to make sure that we have a common understanding around how static files work in Django:

![views and static files]({attach}/img/django-react/views-static.png)

The approach of this guide will be to re-use a lot of this existing setup. We will create an additional that system inserts our React app's JavaScript into a Django static files folder.

![views and static files plus mystery system]({attach}/img/django-react/views-static-mystery.png)

## Why can't we just write React in a single static file?

Why do we need to add a new system? Django is pretty complicated already. Can't we just write our React app in a single JavaScript file like you usually do when writing JavaScript for webpages? The answer is yes, you totally can! You can write a complete React app in a single HTML file:

```html
<html>
<body>
  <!-- React mount point -->
  <div id="app"></div>
  <!-- Download React library scripts -->
  <script crossorigin src="https://unpkg.com/react@16/umd/react.development.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@16/umd/react-dom.development.js"></script>
  <script>
    // Define the React app
    const App = () => {
      const [count, setCount] = React.useState(0)
      const onClick = () => setCount(c => c + 1)
      return React.createElement('div', null,
        React.createElement('h1', null, 'The count is ' + count),
        React.createElement('button', { onClick: onClick }, 'Count'),
      )
    }
    // Mount the app to the mount point.
    const root = document.getElementById('app')
    ReactDOM.render(React.createElement(App, null, null), root)
  </script>
</body>
</html>
```

Why don't we just do this? There are a few issues with this approach of writing React apps:

- We can't use [JSX](https://reactjs.org/docs/introducing-jsx.html) syntax in our JavaScript
- It's harder to break our JavaScript code up into modules
- It's harder to install/use external libraries


<div class="loom-embed"><iframe src="https://www.loom.com/embed/8f2c4c6448144246b25beed21a7b4712" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>


## Webpack

The example code for this section [starts here](https://github.com/MattSegal/django-react-guide/tree/part-1-initial-django) and [ends here](https://github.com/MattSegal/django-react-guide/tree/part-2-add-webpack).

We need a tool that helps us use JSX, and it would be nice to also have a "module bundling system" which lets us install 3rd party libraries and split our JavaScript code up into lots of little files. For this purpose, we're going to use [Webpack](https://webpack.js.org/). Webpack is going to take our code, plus any 3rd party libraries that we want to install and combine them into a single JS file.

![webpack]({attach}/img/django-react/webpack.png)

In this step we will just to create a minimal working Webpack setup. We're not goint try to use React yet. By the end of this section, we won't have added any new JavaScript features, but Webpack will be working.

To use Webpack you need to first install [NodeJS](https://nodejs.org/en/) so that you can run JavaScript outside of your web browser. You need to be able to run `node` and `npm` (the Node Package Manager) before you can continue.

First, go into the example project and create a new folder called `frontend`.
We'll start by just copying over the existing JavaScript that is used by the Django app in [main.js](https://github.com/MattSegal/django-react-guide/blob/part-1-initial-django/backend/todos/static/todos/main.js). We're going to copy this into a "source code" folder at `frontend/src/index.js`.

```javascript
// frontend/src/index.js
const btn = document.getElementById('click')
btn.addEventListener('click', () => alert('You clicked the button!'))
```

Inside of the `frontend` folder, install Webpack using `npm` as follows:

```bash
npm init --yes
npm install webpack webpack-cli
```

Now is a good time to update your `.gitignore` file to exclude `node_modules`. Next, we need to add a file that tells Webpack what to do, which is called `webpack.config.js`

```javascript
// frontend/webpack.config.js
const path = require('path')
const webpack = require('webpack')
module.exports = {
  // Where Webpack looks to load your JavaScript
  entry: {
    main: path.resolve(__dirname, 'src/index.js'),
  },
  mode: 'development',
  // Where Webpack spits out the results (the myapp static folder)
  output: {
    path: path.resolve(__dirname, '../backend/myapp/static/myapp/'),
    filename: '[name].js',
  },
  plugins: [
    // Don't output new files if there is an error
    new webpack.NoEmitOnErrorsPlugin(),
  ],
  // Where find modules that can be imported (eg. React) 
  resolve: {
    extensions: ['*', '.js', '.jsx'],
    modules: [
        path.resolve(__dirname, 'src'),
        path.resolve(__dirname, 'node_modules'),
    ],
  },
}
```

Finally let's make it easy to run Webpack by including an entry in the "scripts" section of our `package.json` file:

```javascript
// frontend/package.json
{
  // ...
  "scripts": {
    "dev": "webpack --watch --config webpack.config.js"
  },
  // ...
}
```

The `--watch` flag is particularly useful: it makes Webpack re-run automatically on file change. Now we can run Webpack using `npm`:

```bash
npm run dev
```

You will now see that the contents of your `main.js` file has been replaced with a crazy looking `eval` statement. If you check your Django app at `http://localhost:8000` you'll see that the JavaScript on the page still works, but it's now using the Webpack build output at `http://localhost:8000/static/myapp/main.js`  

```javascript
// backend/myapp/static/myapp/main.js
eval("const btn = document.getElementById('click')\nbtn.addEventListener('click', () => alert('You clicked the button!'))\n\n\n//# sourceURL=webpack://frontend/./src/index.js?");
```

This file is the Webpack build output. Webpack has taken our source file (`index.js`) and transformed it into an output file (`main.js`): 

![webpack minimal]({attach}/img/django-react/webpack-minimal.png)

So now we have Webpack working. It's not doing anything particularly useful or interesting yet, but all the plumbing has been set up.

<div class="loom-embed"><iframe src="https://www.loom.com/embed/b3dd1325841646a491728c1478a173d3" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>


## Source code vs. build outputs

It's a common newbie mistake to add Webpack build outputs like `main.js` to source control. It's a mistake because source control is for "source code", not "build artifacts". A build artifact is a file created by a build or compliation process. The reason you don't add build artifacts is because they're redundant: they are fully defined by the source code, so adding them just bloats the repo without adding any extra information. Even worse, having a mismatch between source code and build artifacts can create nasty errors that are hard to find. Some examples of build artifacts:

- Python bytecode (.pyc) file,s which are built from .py files by the Python interpeter
- .NET bytecode (.dll) files, built from compiling C# code
- Executable (.exe) files, build from compiling C code

None of these things should go in source control unless there's a special reason to keep them. In general they should be kept out of Git using the `.gitignore` file.

My approach for this project is to create a special Webpack-only folder in Django's static file called "build", which is ignored by Git.
To achieve this, you need to update your `webpack.config.js` file:

```javascript
// frontend/webpack.config.js
// ...
module.exports = {
  // ...
  output: {
      path: path.resolve(__dirname, '../backend/myapp/static/myapp/build/'),
      filename: '[name].js',
  },
  // ...
}
```

You will need to restart Webpack for these changes to take effect. Then you can add `build/` to your `.gitignore` file.
Finally, you will need to update the static file link in your Django template:

```html
{% raw %}
<!-- backend/myapp/templates/myapp/index.html -->
<script src="{% static 'myapp/build/main.js' %}"></script>
{% endraw %}
```

<div class="loom-embed"><iframe src="https://www.loom.com/embed/86893cc2f3c14a41ab347bc912678ec9" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

## Adding React

The example code for this section [starts here](https://github.com/MattSegal/django-react-guide/tree/part-2-add-webpack) and [ends here](https://github.com/MattSegal/django-react-guide/tree/part-3-add-babel-and-react).

Now that Webpack is working, we can add React. Let's start by installing React in our `frontend` folder:

```bash
npm install react react-dom
```

Now we can use React in our JavaScript source code. Let's re-use the small counter app I created earlier:

```jsx
// frontend/src/index.js
import React from 'react'
import ReactDOM from 'react-dom'

// Define the React app
const App = () => {
  const [count, setCount] = React.useState(0)
  const onClick = () => setCount(c => c + 1)
  return React.createElement('div', null,
    React.createElement('h1', null, 'The count is ' + count),
    React.createElement('button', { onClick: onClick }, 'Count'),
  )
}
// Mount the app to the mount point.
const root = document.getElementById('app')
ReactDOM.render(React.createElement(App, null, null), root)
```

Now if you go to `http://localhost:8000/` you should see a simple counter. If you inspect the contents of `main.js` at `http://localhost:8000/static/myapp/build/main.js`, you'll see that there is a *lot* more stuff included in the file. This is because Webpack has bundled up our code plus the development versions of React and ReactDOM into a single file:


![webpack]({attach}/img/django-react/webpack.png)

<div class="loom-embed"><iframe src="https://www.loom.com/embed/76bf5c576ff148aea4e0d332507ec381" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

{% from 'mail.html' import mailchimp %}
{{ mailchimp("Get alerted when I publish new blog posts", "Enter your email address", "Subscribe") }}

## Adding Babel

Next we need at tool that lets us write JSX. We want to be able to write our React components like this:

```jsx
const App = () => {
  const [count, setCount] = React.useState(0)
  const onClick = () => setCount(c => c + 1)
  return (
    <div>
      <h1>The count is {count}</h1>
      <button onClick={onClick}>Count</button>
    </div>
  )
}
```

and then some magic tool transforms it into regular JavaScript, like this:

```jsx
const App = () => {
  const [count, setCount] = React.useState(0)
  const onClick = () => setCount(c => c + 1)
  return React.createElement('div', null,
    React.createElement('h1', null, 'The count is ' + count),
    React.createElement('button', { onClick: onClick }, 'Count'),
  )
}
```

That magic tool is [Babel](https://babeljs.io/), a JavaScript compiler that can transform JSX into standard JavaScript.
Babel can use [plugins](https://babeljs.io/docs/en/plugins), which apply custom transforms to your source code.
It also offers [presets](https://babeljs.io/docs/en/presets), which are groups of plugins that work well together to achieve a goal.

Now we're going to install a whole bunch of Babel stuff with `npm`:

```bash
npm install --save-dev babel-loader @babel/core @babel/preset-react
```

What the hell is all of this? Let me break it down for you:

- **[@babel/core](https://babeljs.io/docs/en/babel-core)**: The main Babel compiler library
- **[@babel/preset-react](https://babeljs.io/docs/en/babel-preset-react)**: A collection of React plugins: tranforms JSX to regular JavaScript
- **[babel-loader](https://github.com/babel/babel-loader)**: Allows Webpack to use Babel

These are not the only Babel plugins that I like to use, but I didn't want to add too many new things at once.
In addition to installing the plugins/presets, we need to tell Babel to use them, which we do with a config file called `.babelrc`.

```javascript
// frontend/.babelrc
{
    "presets": ["@babel/preset-react"]
}
```

Next, we need to tell Webpack to use our new Babel compiler for all our JavaScript files:

```javascript
// frontend/webpack.config.js
// ...
module.exports = {
  // ...
	// Add a rule so Webpack reads JS with Babel
	module: { rules: [
    {
      test: /\.js$/,
      exclude: /node_modules/,
      use: ['babel-loader'],
    },
  ]},
  // ...
```

Essentially, this config change tells Webpack: "for any file ending with `.js`, use `babel-loader` on that file, expect for anything in `node_modules`".
Finally, we can now use JSX in our React app:

```jsx
// frontend/src/index.js
import React from 'react'
import ReactDOM from 'react-dom'

// Define the React app
const App = () => {
  const [count, setCount] = React.useState(0)
  const onClick = () => setCount(c => c + 1)
  return (
    <div>
      <h1>The count is {count}</h1>
      <button onClick={onClick}>Count</button>
    </div>
  )
}
// Mount the app to the mount point.
const root = document.getElementById('app')
ReactDOM.render(<App />, root)
```

You will need to restart Webpack for the config changes to be loaded. After that, you should be able to visit `http://localhost:8000/` and view your counter app, now working with JSX.


<div class="loom-embed"><iframe src="https://www.loom.com/embed/18e5b20ee31344b588aa17dd902344ce" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>


## Deployment

I won't cover deployment in detail in this post, because it's long enough already, but in short, you can now deploy your Django/React app as follows:

- Install JavaScript dependencies with `npm`
- Run Webpack to create build artifacts in your Django static files
- Deploy Django how you normally would

There a few things that it would be good to change before deploying, like not using "development" mode in Webpack, but this workflow should get you started for now.
If you have never deployed a Django app before, I've written an [introductory guide](https://mattsegal.dev/simple-django-deployment.html) on that as well, which uses the same incremental, explanation-heavy style as this guide.

## Next steps

There is a **lot** of stuff I didn't cover in this guide, which I'd like to write about in the future. Here are some things that I didn't cover, which are important or useful when building a React/Django app:

- Hot reloading
- Deployment
- Passing requests/data between Django and React
- Modular CSS / SCSS / styled components
- Routing and code-splitting
- Authentication
