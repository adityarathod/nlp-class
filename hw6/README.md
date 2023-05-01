# Homework 6: Web Scraping + Knowledge Bases

## Part 1: Knowledge base creation

The knowledge base was created using a hybrid method of sourcing data from my domain knowledge and utilizing external APIs to provide data that would be continuously updated regarding the subject matter.

First, I determined the top 10 terms manually using a mix of frequency analysis and domain knowledge:

```
skin
champion
player
team
attack
ad
ap
rift
effect
esports
```

I then wrote definitions for each of these terms in JSON format:

```json
{
	"skin": "A non-functional, cosmetic modification to a character model in-game. Serves as the primary form of microtransactions in League of Legends.",
	"champion": "A playable character in League of Legends. Each champion has its own lore, abilities, mechanics, skins, itemization, and role in the game.",
	"player": "A user of League of Legends. There are 10 players in a standard game of League. There are approximately 150 million monthly active players.",
	"team": "A group of (currently) five players, each playing distinct champions, who are partnered together in a game.",
	"attack": "Any action of a character that deals damage to another champion, neutral objective, or jungle monster.",
	"ad": "Standing for Attack Damage, is a stat of characters that determines how much damage is dealt via basic attacks (and in some cases, abilities too).",
	"ap": "Standing for Ability Power, is a stat of characters that determines how much damage is dealt via abilities.",
	"rift": "Short for 'Summoner's Rift,' this corresponds to one of the two permanent maps where League is played. The Rift is a three-lane map separated by the jungle and split between two teams via a river.",
	"effect": "Could refer to a status effect in League of Legends. Most status effects fall into the buff or debuff categories. For instance, destroying the red brambleback provides you the 'red buff,' while claiming the Dragon Soul provides you various other buffs. Debuffs are usually in the form of crowd control.",
	"esports": "League of Legends has a massive esports scene, driven by its large player base. LoL Esports is split into multiple levels, with the highest being the professional teams in each geographic region (e.g. LCS, LCK, LPL, LEC)."
}
```

I used JSON over pickling because it provided ease in adding new terms to the knowledge base as needed.

Additionally, I augmented a lot of this data using LoL API data on champions, skins, and AD/AP ratios for each champion in the game.

Using their [Data Dragon API](https://developer.riotgames.com/docs/lol#data-dragon_champions) I was able to put together a simple test prototype in which a user can enter a champion and see the information stored by Riot about the champion, and even view each skin:

```bash
$ python kb_test.py

LoL Knowledge Base Tester
-------------------------
Pick an option:
[1] Get top 10 term definition
[2] Get champion data
[3] Get champion skins

Option [type 'q' to quit]: 2

Champion Data Resolver
------------------------
Enter a champion ID to get its data
Champion ID: Belveth
Data:
{'type': 'champion', 'format': 'standAloneComplex', 'version': '13.5.1', 'data': {'Belveth': {'id': 'Belveth', 'key': '200', 'name': "Bel'Veth", 'title': 'the Empress of the Void', 'image': {'full': 'Belveth.png', 'sprite': 'champion0.png', 'group': 'champion', 'x': 144, 'y': 48, 'w': 48, 'h': 48}, <output truncated...> }}
------------------------

Option [type 'q' to quit]: 3

Champion Skins Resolver
------------------------
Enter a champion ID to get its skins.
Champion ID: Belveth
Skins:
['default', "Battle Boss Bel'Veth"]
------------------------

Option [type 'q' to quit]: q
```

## Part 2: Future knowledge base usage

In the future, I would like to use this knowledge base to ask the following questions. Note the unclean nature of the user input.

```
User: Can I get the lore for Aatrox?
Bot: Sure, here's a bit about Aatrox:

Once honored defenders of Shurima against the Void, Aatrox and his brethren would eventually become an even greater threat to Runeterra, and were defeated only by cunning mortal sorcery. But after centuries of imprisonment, Aatrox was the first to find freedom once more, corrupting and transforming those foolish enough to try and wield the magical weapon that contained his essence. Now, with stolen flesh, he walks Runeterra in a brutal approximation of his previous form, seeking an apocalyptic and long overdue vengeance.

User: aatrox passive what does it do
Bot: Aatrox's passive, called Deathbringer Stance, does this:
    
Periodically, Aatrox's next basic attack deals bonus physical damage and heals him, based on the target's max health.

User: How many champions in game
Bot: There are 162 champions in the game right now.
```