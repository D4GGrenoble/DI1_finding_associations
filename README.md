# Finding associations in France
A repository for work conducted during DataInsight Event #1 which aims to find information about associations/charities in France.

## Data
There is a list of all associations curretnly registered in France. The data originates here: https://www.data.gouv.fr/fr/datasets/repertoire-national-des-associations/


We have a cleaner and cutdown version here which is much easier to look at for our purposes:
https://drive.google.com/open?id=1Xw16znqORPuCdRw-kSWhMr_Zsb0Te9w3


This cleaner version has:
- only the currently active associations
- only the address where the activity is taking place (not the headquarters)
- added a column with the definition of objet_social1 (the purpose selected from a standard list - which was originally encoded as a number)
- removed fields which we dont understand how they can be used
- removed bad lines

## Housekeeping
I suggest that we keep this repo tidy by:
- keep information that may be useful to others in the main folder
- place our own scripts in a folder with our own name/name of work in it

I think there will be lots of jupyter notebooks which can cause conflicts, so please do not push other peoples notebooks that you have opened but not edited!

If you are not sure how to contribute your code speak to Brad :)

## Contributors

* **Jean-Baptiste Barre** - [jbbarre](https://github.com/jbbarre)
* **Myriam Begel** - [mbegel](https://github.com/mbegel)
* **Thibaud Godon** - [thibgo](https://github.com/thibgo)
* **Brad Keogh** - [keoghdata](https://github.com/keoghdata)
* **Mehdi Mediouni**
* **Shachar Mirkin**
* **Pierre Pereira**
* **Sung-Ho**
* **Younes Zaibila**
