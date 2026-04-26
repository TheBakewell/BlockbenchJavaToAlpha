# BlockbenchJavaToAlpha
A tool that allows converting Blockbench .java models for Minecraft 1.17+ into models that work with decompiled Minecraft Alpha.

# How to use
Open the Exe file, browse for your .java file made for Minecraft 1.17+, add it, and convert it.
The converted file will end up at the same place as where the original file was at.

# Usage for decompiled file
Import this file into your Minecraft Alpha 1.1.2_01 or similar version project, and set up the Model(Entityname), Render(Entityname), and Entity(entityname). I have only tested this using "AlphaMCP2" for decompilation. You may need to patch RenderEngine to support larger textures if you are using texture sizes larger than 256x256, specifically allowing the ByteBuffer "imageData" to be larger

# Currently known problems
- May rarely not convert a couple cubes on more complex models, or on models with duplicated parts.
