<p align="center">
  <img src="https://ubistatic19-a.akamaihd.net/ubicomstatic/de-de/global/search-thumbnail/trackmania_search_362083.jpg"/>
  <p align="center"><em>Unofficial Trackmania 2020 integration for Blender.</em></p>
</p>

---

# Blender Trackmania Tools

You want to create custom Items for Trackmania 2020 using Blender, but you don't want to fiddle with NadeoImporters XML files? This Blender-Addon integrates the NadeoImporter into Blender and packs it into a handy Export-button!

## Example

<p align="center">
  <img src="https://user-images.githubusercontent.com/11406580/107148256-943a1000-6952-11eb-9962-38fc3eeab305.png" width="75%" height="75%">
  <img src="https://user-images.githubusercontent.com/11406580/107148644-acab2a00-6954-11eb-9bbc-8f5f19b7192c.png" width="75%" height="75%">
  <img src="https://user-images.githubusercontent.com/11406580/107148658-bb91dc80-6954-11eb-945b-081fbcdaa877.png" width="75%" height="75%">
</p>

## Installation

To use this addon, you need to do two things:

 1. Download the NadeoImporter from here: https://nadeo-download.cdn.ubi.com/trackmania/NadeoImporter_2021_01_19.zip
 2. Extract the NadeoImporter to your games install-location, so that all files are in the same folder as `Trackmania.exe`. 
 
    As of now, it *has* to be one of the following paths: (Other locations will not work!)
 
    - `C:\Program Files\Epic Games\TrackmaniaNext`
    - `C:\Program Files\Ubisoft\Ubisoft Game Launcher\games\Trackmania`
    - `C:\Program Files\Trackmania`
    
 3. Download the [latest release of the Addon (TrackmaniaExport.py)](https://github.com/ataulien/blender-trackmania-tools/releases/latest)
 4. In Blender, go to *Edit* -> *Preferences* -> *Add-Ons* -> *Install...* and select the addon file you just downloaded.

    <p align="center">
      <img src="https://user-images.githubusercontent.com/11406580/107147551-f5f87b00-694e-11eb-8cbd-082abfffdc56.png" width="75%" height="75%"/>
    </p>

 5. Search for `Trackmania` and enable the addon! (Make sure you are in the *Community*-tab)
 
    <p align="center">
      <img src="https://user-images.githubusercontent.com/11406580/107147618-4d96e680-694f-11eb-8546-9962eba1f5b0.png" width="75%" height="75%"/>
    </p>
    
## Usage

Create your model in Blender as usual, then export it as *Trackmania Item (.item.gbx)*.

<p align="center">
  <img src="https://user-images.githubusercontent.com/11406580/107147681-9f3f7100-694f-11eb-9596-5e85a6683bcc.png" width="75%" height="75%"/>
</p>

The NadeoImporter requires the files to be put at very specific locations. Therefore, you don't need to chose a location, as the Addon will handle that for you.

## Where are the exported files?

The finished Items will be placed at `Documents\Trackmania\Items\BlenderTrackmaniaExport`.

## How to change Materials?

The Addon is still lacking in this regard, as it won't show all the available materials and does not have the corresponding textures. 
However, if you name your Blender material one of the following, the correct material will be used ingame:

 - `PlatformTech`,`Grass`,`Pylon`,`RoadBump`,`RoadDirt`,`RoadIce`,`RoadTech`,`TrackWall`,
 - `ItemPillar`,`ItemBase`,`CustomBricks`,`CustomConcrete`,`CustomDirt`,`CustomGrass`,
 - `CustomIce`,`CustomMetal`,`CustomPlastic`,`CustomRock`,`CustomRoughWood`,`CustomSand`,
 - `CustomSnow`,`DecoHill`,`TrackBorders`,`DecalCurbs`,`DecalMarks`,`DecalMarksRamp`,
 - `DecalMarksStart`,`DecalSpecialTurbo`,`DecalSponsor1x1BigA`,`ItemBorder`,`ItemCactus`,
 - `ItemLamp`,`ItemRamp`,`ItemRoadSign`,`ItemTrackBarrier`,`ItemTrackBarrierB`,`ItemTrackBarrierC`,
 - `Speedometer`,`SpeedometerLight_Dyna`,`SyntheticFloor`,`Technics`,`TechnicsTrims`,`TrackWallClips`
 
## UV-Layers
 
If the Addon finds that your meshes are lacking the UV-layers required by the NadeoImporter, it will modify the meshes so 
they conform to what the NadeoImporter expects. You may need to tweak th UV-layers afterwards if you find your lighting to look bad.
 
## Icons
 
The Addon will automatically use Blender to render an Icon for your Item. If you want the Icon to look somewhat good, you should posision the camera properly and add some lighting. Sun-lights will not be exported into the Items and are therefore good to make the Icon look pretty.

## Known Issues

This Addon is still under development, here are some known issues/shortcommings/planned features:

 - Currently no way to use custom textures
 - Blender should show the games textures on the models
 - Game install location is fixed, should be configurable
 - Can the NadeoImporter be shipped with the addon? Does it need to be put into the TM install folder?
 - Make custom properties to select Physics ID, Gameplay ID, etc
