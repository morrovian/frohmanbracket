# frohmanbracket

This is a Mathematica file. Using it requires a Mathematica subscription. To use, download the folder as a ZIP, extract the folder, and open the .nb file. Necessary information is contained in the notebook.

Alternatively, for those who use Python or want to read the code (Mathematica notebooks don't look pretty on Github), I translated it into Python in Tangela.py.

If you are simply experimenting on the code, download Tangela.py and run it. You essentially have two options for computing a polynomial.

If you're trying to compute the polynomial of a knot you already have some info about (like it's listing in the knot table), you can look
up the braid notation at https://knotinfo.math.indiana.edu/index2.php to get the fastest results.

E.g. a figure-eight in KnotInfo has braid notation {1,-2,1,-2}. Run this in Tangela.py as "slthree_braid([1,-2,1,-2])" to get "1y^18 - 1y^6 + 1 - 1y^-6 + 1y^-18". Notice that in KnotInfo, the notation is in curly brackets, but in Python, it is put in as square brackets.

For a link, the braid notation is similar but, importantly, is a nested array. Take, for example, the Borromean rings, one variation of which is in KnotInfo as L6a4{1,1}. The braid notation is given as {3,{1,-2,1,-2,1,-2}}. Run this in Python as "slthree_braid([3,[1,-2,1,-2,1,-2]])" to get "-1y^24 + 2y^18 + 1y^12 + 5 + 1y^-12 + 2y^-18 - 1y^-24".


Braid notation is not so useful if you just drew a knot/link and need to compute the invariant. That's where extended Gauss notation comes in. https://knotinfo.math.indiana.edu/descriptions/gauss_notation.html

Importantly, I am talking about extended Gauss code, NOT normal Gauss code, as this is not an invariant. In the example of the trefoil knot, with Gauss code "[1,-2,3,1,2,3]", I get "-1y^12 + 1 + 1y^-12".

I am continually working on improving this code. As of April 2023, I believe that using Conway notation can greatly optimize this algorithm, but with heavy coursework and interviews, I won't be looking into this until June.
