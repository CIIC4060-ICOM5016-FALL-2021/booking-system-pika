# Booking Frontend

Designed with React

The way user performs a booking is the following:

- Login -> enter user credentials
- User Dashboard

In this dashboard there's a bunch of things the person can see. There's an option to create a new booking,
manage current bookings, statistics, and a simple search engine.

The first thing the user sees are statistics of the bookings that has done, the most frequent booked rooms, any upcomming
meeting this user may have, the people who this person books most things, and any other required statistics.

On the create new booking section you'll see it follows a linear-step-by-step form for the sake of simplicity for both
the person who may be using this, and most importantly, the ones maintaining this. 

Here's a step-by-step process of how the person would book a room:

1. select the people you want to invite.You get a panel of the people around (kinda like boxes), you select the ones you
want in the booking.
2. Then You select the day, the hour and the duration of this booking. If any of the invited have either a conflict
because they have a another meeting on that time OR they selected the option of being unavailable at that time
or near it (hours collide). Then you cannot continue. For the person's sake, the app will show in green light in
a calendar the time where everyone is available, and red hues where there's a conflict. 
3. Once you've picked the time, you find a room selection. All rooms shown are those that are available within the specified
time. 
4. Finally, you can add a message, file or image that could either lead to the details of the booking for the invitees
or that the invitees would be aware of.

### Stuff

Just like you have Models and Controllers in the backend (flask), in ReactJS you have components, which are kinda like
headers.

Since react is very very large, we used a bunch of UI libraries because our mental health comes first, the client's
stupidity second :)

The first library we used was ```react big calendar```


```Rechart```

### How we handle passowrds

Because this is a college project, we didn't messed around with outh. So prolly afterwards one of the team members would
make a branch or something and maybe add it on its free time on vacations or something. For now, we used a password query
as was adviced to keep things simple.



Usa react big calendar (DOCUMENTATION)










# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\]
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
