CONFIG_TEMPLATE = '''{
    // To generate default config, delete config file and launch a game again

    // Global features toggle
    // Valid values: true/false (default: true)
    //
    // When set to false, it globally disables all features of this mod
    // however it does not remove mod presence itself.
    "enabled": %(enabled)s,

    // Valid values: ["en", "de"]
    // Default value: "de"
    //
    // Language used by the mod interface:
    // - "en" - Englisch,
    // - "de" - Deutsch.
    "mod-language": %(mod-language)s,

    // Valid values: ["always", "on-alt-pressed"]
    // Default value: "always"
    //
    // Configures when marker should be displayed:
    // - "always"         - displays marker always,
    // - "on-alt-pressed" - when ALT key is being pressed.
    "display-mode": %(display-mode)s,

    // Valid values: ["ally-and-enemy", "only-enemy"]
    // Default value: "only-enemy"
    //
    // Configures for which tanks marker should be displayed:
    // - "ally-and-enemy" - for all tanks,
    // - "only-enemy"     - only for enemies.
    "marker-target": %(marker-target)s,

    // Valid values: ["tank-marker", "tank-center", "tank-bottom"]
    // Default value: "tank-bottom"
    //
    // Position at which markers are initially displayed with zero offsets:
    // - "tank-marker" - at standard tank marker position,
    // - "tank-center" - at tank center position,
    // - "tank-bottom" - at tank bottom position.
    "anchor-position": %(anchor-position)s,

    // Valid values: true/false (default: true)
    //
    // When set to true, marker position can no longer be edited during battle.
    // Useful if you want to prevent accidental change.
    "lock-position-offsets": %(lock-position-offsets)s,

    // Valid values: integer between -150 and 150 (default 0)
    //
    // Controls horizontal marker offset relative to anchor position, in pixels.
    // Positive values moves marker to right side, negative values - to left side.
    //
    // Hint: Offsets can be visually edited during battle by dragging markers
    // with mouse while CTRL key is being held.
    // Offsets will be saved in configuration on battle finish or manual exit.
    "anchor-horizontal-offset": %(anchor-horizontal-offset)s,

    // Valid values: integer between -150 and 150 (default 0)
    //
    // Controls vertical marker offset relative to anchor position, in pixels.
    // Positive values moves marker upwards, negative values - downwards.
    //
    // Hint: Offsets can be visually edited during battle by dragging markers
    // with mouse while CTRL key is being held.
    // Offsets will be saved in configuration on battle finish or manual exit.
    "anchor-vertical-offset": %(anchor-vertical-offset)s,

    // Valid values: integer between 0 and 3 (default 0)
    //
    // Decimal precision of displayed distance.
    "decimal-precision": %(decimal-precision)s,

    // Valid values: integer between 6 and 24 (default 11)
    //
    // Base size of text displayed in marker.
    // According to distance it is increased by zone specific bonus values.
    "text-size": %(text-size)s,

    // Valid values: number between 0.0 and 1.0 (default 0.9)
    //
    // Controls transparency of text in markers:
    // - value 1.0 means full visibility,
    // - value 0.0 means zero visibility.
    "text-alpha": %(text-alpha)s,

    // Valid values: true/false (default: true)
    //
    // When set to true, text is additionally displayed with black outline.
    // Very useful when text blends with arbitrary shapes (for example: hover icon of vehicle markers).
    "draw-text-outline": %(draw-text-outline)s,

    // Valid values: true/false (default: false)
    //
    // When set to true, text is additionally displayed with smooth gradient shadow.
    // Useful when text blends with background.
    "draw-text-shadow": %(draw-text-shadow)s,

    // Valid values: true/false (default: false)
    //
    // When set to true, distance is additionally displayed with meter unit (like "420 m").
    "draw-distance-unit": %(draw-distance-unit)s,

    // Valid values: always-symbol, except-view-range, always-numbers
    //
    // The default uses "^" except around view-circle changes.
    "imprecise-display-mode": %(imprecise-display-mode)s,

    // Text color used for distances between 51 and 175 m.
    // Valid value: 3-element array of numbers between 0 and 255
    // Default value: [255, 11, 0] (this is red color)
    "text-color": %(text-color)s,

    // Text color used for distances up to 50 m.
    // Valid value: 3-element array of numbers between 0 and 255
    // Default value: [0, 153, 255] (cyan-blue color)
    "near-distance-color": %(near-distance-color)s,

    // Text color used for distances between 176 and 250 m.
    // Valid value: 3-element array of numbers between 0 and 255
    // Default value: [255, 11, 0] (this is red color)
    "zone3-distance-color": %(zone3-distance-color)s,

    // Text color used for distances between 251 and 300 m.
    // Valid value: 3-element array of numbers between 0 and 255
    // Default value: [255, 11, 0] (this is red color)
    "zone4-distance-color": %(zone4-distance-color)s,

    // Text color used for distances between 301 and 445 m.
    // Valid value: 3-element array of numbers between 0 and 255
    // Default value: [255, 11, 0] (this is red color)
    "zone5-distance-color": %(zone5-distance-color)s,

    // Text color used for distances further than 445 m.
    // Valid value: 3-element array of numbers between 0 and 255
    // Default value: [255, 229, 0] (orange color)
    "far-distance-color": %(far-distance-color)s,

    // Valid values: integer between 0 and 25 (default 7)
    //
    // Additional text size bonus for distances up to 50 m.
    "size-bonus-zone1": %(size-bonus-zone1)s,

    // Valid values: integer between 0 and 25 (default 5)
    //
    // Additional text size bonus for distances between 51 and 175 m.
    "size-bonus-zone2": %(size-bonus-zone2)s,

    // Valid values: integer between 0 and 25 (default 4)
    //
    // Additional text size bonus for distances between 176 and 250 m.
    "size-bonus-zone3": %(size-bonus-zone3)s,

    // Valid values: integer between 0 and 25 (default 3)
    //
    // Additional text size bonus for distances between 251 and 300 m.
    "size-bonus-zone4": %(size-bonus-zone4)s,

    // Valid values: integer between 0 and 25 (default 2)
    //
    // Additional text size bonus for distances between 301 and 445 m.
    "size-bonus-zone5": %(size-bonus-zone5)s,

    // Valid values: integer between 0 and 25 (default 0)
    //
    // Additional text size summand for distances further than 445 m.
    "size-bonus-zone6": %(size-bonus-zone6)s,

    // DO NOT touch "__version__" field
    // It is used by me to seamlessly update config file :)
    "__version__": 5
}
'''
