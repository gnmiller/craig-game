# Changelog

## Unreleased

## Planned

    - Move fishing sell to inventory commands
    - equipping items from inventory

## [0.0.1] - 2023-08-11

### Added
    
    - Stats as attributes in Character
        - ex Character.strength returns Character.stats.strength
    - Fishing! Basic support for fishing added.
        - /fishing commands added and beginning steps to implement
        - Fish and FishingPool new classes for supporting fishing
    - Inventory commands! You can now see what you have in your bages.
    - Added some commands to admin for managing/testing (set_exp, set_gold)

### Changed

    - Character.level returns and expects level as int and no longer
        character.Level
    - Better support for gold and items in inventory
        - get_gold() and is_empty
    - Functionality for experience to Characters and related classes
        - Character.gain_exp(value), Level.check_next(), etc
        - now included in __str__
    - General documentation improvements

### Deprecated

### Removed

### Fixed

    - Inventory.del_item() bug fixes
        - Should work correctly now when any items are present

### Security

