# MacGyver

Duct Tape and a Swiss Army Knife. Angular helpers for all your friends!

[![Build Status](http://img.shields.io/travis/angular-macgyver/MacGyver.svg?style=flat-square)](https://travis-ci.org/angular-macgyver/MacGyver)
[![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](https://github.com/angular-macgyver/MacGyver/blob/master/LICENSE)
[![Latest Release](http://img.shields.io/github/release/angular-macgyver/MacGyver.svg?style=flat-square)](https://github.com/angular-macgyver/MacGyver/releases/latest)

[![Selenium Test Status](https://saucelabs.com/browser-matrix/macgyver-ci.svg)](https://saucelabs.com/u/macgyver-ci)

## Components ##

### Directives ###
 - Affix
 - Autocomplete
 - Canvas Spinner
 - Events
 - Menu
 - Modal
 - Placeholder
 - Popover
 - Scroll Spy
 - Spinner
 - Tag Autocomplete
 - Time Input
 - Tooltip

### Filters ###
 - Boolean
 - Pluralize
 - Timestamp
 - Underscore String

## 3rd party libraries dependencies ##
 - AngularJS (1.2.x+)
 - Underscore String (Underscore string filter)

## Using MacGyver ##
You can install via [Bower](http://www.bower.io) or download from [Github](https://github.com/angular-macgyver/MacGyver/archive/master.zip)

To install via bower, make sure you have bower installed and then run:

```
bower install angular-macgyver
```

More bower repositories can be found at [Angular MacGyver](https://github.com/angular-macgyver)

Once you have MacGyver in your project, just include "Mac" as a dependency in your Angular application and you’re good to go.

```javascript
angular.module("myModule", ["Mac"]);
```

MacGyver includes multiple files,
- `macgyver.js` - All directives, services and filters bundled together
- `macgyver-core.js` - Utilities, events and all directives without 3rd party dependencies
- `macgyver-filters.js` - Filters except underscore string filter
- `macgyver-string-filter.js` - Underscore String filter
