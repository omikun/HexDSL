# OrbitalDom

A prototype of a different kind of Civ-like turn based game with a more board game like experience and a more realistic depiction of modern day geo-politics.

## Overview

### Win Conditions

There are multiple win conditions:

    - Attain singularity first; requires
        - top level tech researched
        - infrastructure to support AI seed
        - economic engine to support scaling
        - military defense until AI is omnipotent
    - Military conquest
        - Subjugation of other nations by force
        - Must undermine strong adversaries from within, by trickery, and by deceit
        - Break enemy alliances, destroy trust, build support in shadows
    - Escape
        - Turtle and build infrastructure to colonize the moon, Mars, and then the stars
        - Escape faster than enemy military or singularity can catch you
        - Enlist alien deus ex machina

### Mechanics

Resources (political, financial, technological, etc) are controlled by multiple entities within and across countries. Politics is the negotiation in resource distribution and control. In order to harness the necessary resources, you harness political will.

You play as the puppet master, independent of who is in elected or is in charge.

Each nation must manage and compete on multiple overlapping realms:

    - Politics - 
        - All governments are some variations of democracy:
            - US has 2 levels of democracy, public and senate:
                - the public elect each senator/president together
                    - TODO partition public to states
                - all senators vote on bills
                - president can veto bill or sign it
            - China has 1 level of democracy, party:
                - individual party members can be replaced at any time by president
                - party members elect president
                - strong bias towards president
            - Russia has 1 level of democracy, public:
                - public strongly biased towards Putin, 
                - bias must be replenished with propaganda spending
        - All governments can:
            - Influence democracy via:
                - Propaganda
                    - can backfire if exposed
                    - uniformly influence population
                    - shift average opinion
                    - takes 1 or more turn to take into effect
                    - can make up stronger negative propaganda, but w/o proof, produces backfire propaganda that can be leaked or stolen
                - influence specific individuals temporarily or permanently
                    - bribery - costs financial capital
                    - blackmail - costs intelligence capital
                    - coerce - costs political capital
                    - favor - can be anything a player can do
                        - do immediately or at a later turn, with repercussions if not honored
                        - manipulate another senator, propaganda, add rider to bill, declare war, etc
                    - random chance not work, but more likely to work next time
                    - increases influence meter, threshold is random
                    - others can counter influence or change threshold
                    - influence degrade per turn
                    - assassination
                        - produces secret negative propaganda; any intelligence can use, non-zero chance of leaking to press, can reduce chance with more intelligence spending, propanganda
    - Economics - 
        - Manipulate GDP 
            - propaganda can change stock prices
                - indirectly influences GDP
            - gov programs to increase specific industry's productivity
            - gov research program to increase overall productivity, new products
            - interest rates increase growth rates for all industries
            - steal foreign tech and give to industries
            - tax loophole for private research
        - trade
            - more export in industry expands that industry
            - larger industry have lower costs
            - price changes implemented as random walk, 
                - price bounds changes with supply/demand
                - bounds shrink with stability
                    - stability inversely related to public trust in industry/country
        - Manipulate trade
            - tax import/export to discourage trade
            - reduce total trade via law/alliance (economic sanction)
            - negative tax to encourage trade
    - Industries
        - space, food, manufactuer, mining, recycler, energy, tech, 
            - TODO: entertainment, service, education, healthcare
            - Maybe? transport, tech AND robotics?
        - each industry 
            - consumes products, generates waste equivalent to PR
            - requires some labor of some skill level per unit size
            - has some productivity per unit size
            - all industries form a complete dependency cycle
        - mining extracts ore from country (each country has some finite amount)
        - manufactuer converts ore to usable products 
            - either sold to population or to other industries
        - used products turn into waste, recyclers can convert some percentage of this back to ore
        - manufactuer req miners
        - types of physical resources
            - oil
            - ore
            - rare ore
        - manufactuers can turn PR to chemical, alloys, semiconductors, exotics
        - transport needs oil and alloys
        - tech needs semiconductors
        - space needs alloys and exotics and tech
        - robotics needs tech and alloys
        - recycler needs waste
    - Industry
        - consumes some energy, goods, requires some labor
        - labor can be supplanted/replaced with robotics
        - tech can reduce need for goods and labor and energy
        - labor divided by skills
        - labor costs determined by supply/demand and worker health
        - worker age determines amount of service required
        - 

    - Citizens
        - requires service, changes with age/health
        - consumes food, entertainment, 
        - has happiness, skill, trust, 
    - Intelligence -
        - Steal foreign tech
        - identify foreign influence on senators/public
        - blackmail foreign/domestic politicians
        - find negative propaganda to use
