# Settings review

The integrated browser build now provides:

| Group | Option | Current behavior |
| --- | --- | --- |
| Audio | Background tone and level | A low procedural tone starts after Play is pressed, varies by 100-level region and remaining light, and can be disabled or adjusted. This is a preview of the planned score. |
| Audio | Sound effects and level | Separately enables and scales move, delivery, hazard, success, and failure cues. |
| Controls | Haptics | Enables existing vibration patterns on supported phones; browsers and devices may ignore vibration. |
| Display | Storybook, Isometric, Night | Storybook is the initial view. Changing the view does not change the route or shadow rules. |
| Comfort | Reduce motion | Removes UI animation and shortens board travel animation. |
| Comfort | Stronger move cues | Adds outlines to safe and blocked neighboring tiles. |
| Help | Show level guide | Opens the current level's explanation on demand. |

These choices are stored in the local campaign save. The wardrobe selection is stored separately; shadow appearance is automatically assigned by district from `design/shadow-variants/region-shadow-map.json`.

Reference review: [Sky's official Settings guide](https://thatgamecompany.helpshift.com/hc/en/17-sky-children-of-the-light/faq/523-how-do-i-access-the-utility-settings-menu-how-do-i-change-my-game-settings/) describes separate audio levels, vibration, controls, and graphics options. [King's Candy Crush Soda accessibility announcement](https://community.king.com/en/candy-crush-soda-saga/discussion/445124/celebrate-the-global-accessibility-awareness-day-with-soda) describes music/effects sliders and extra audio and visual accessibility controls. We kept the options that correspond to features currently in this game. Mono/balance controls, notifications, account/cloud controls, and graphics/FPS settings need corresponding audio, online, or native rendering support before they should appear as active options.
