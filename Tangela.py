import numpy

##The following are basic support functions and do not pertain directly to knot theory
def make_twolist(value, i, j):
  mid = [value]*i
  fin = []
  for x in range(j):
    fin.append(dcopy(mid))
  return fin
  

def dcopy(x):
  if (type(x) == list):
    newx = []
    for elem in x:
      if ((type(elem) == list) or (type(elem) == dict)):
        newx.append(dcopy(elem))
      else:
        newx.append(elem)
    return newx
  if (type(x) == dict):
    newx = {}
    for elem in x:
      if ((type(x[elem]) == list) or (type(x[elem]) == dict)):
        newx[elem] = dcopy(x[elem])
      else:
        newx[elem] = x[elem]
    return newx
  return x
  

def abslist(alist):
  blist = dcopy(alist)
  for x in range(len(blist)):
    if (type(blist[x]) == list):
      blist[x] = abslist(blist[x])
    else:
      blist[x] = abs(blist[x])
  return blist
def flatten(alist):
  if (type(alist) != list):
    return [alist]
  newlist = []
  for elem in alist:
    newlist = newlist + flatten(elem)
  return newlist

def sign(num):
  if (num > 0):
    return 1
  if (num < 0):
    return -1
  return 0

def listmult(alist,num):
  blist = dcopy(alist)
  for x in range(len(blist)):
    if (type(blist[x]) == list):
      blist[x] = listmult(blist[x],num)
    else:
      blist[x] = blist[x]*num
  return blist

def add_absint_to_list(alist, num):
  blist = dcopy(alist)
  for x in range(len(blist)):
    if (type(blist[x]) == list):
      blist[x] = add_absint_to_list(blist[x],num)
    else:
      if (blist[x] > 0):
        blist[x] = blist[x] + num
      else:
        blist[x] = blist[x] - num
  return blist

##beginning of more complex functions



#This is a polynomial class
class Poly:
  #nes contains negative exponents, nonnes contains nonnegatives
  nes = []
  nonnes = []
  def term(self, pow):
    if (pow < 0):
      if (abs(pow) > len(self.nes)):
        return 0
      else:
        return self.nes[abs(pow) - 1]
    else:
      if (pow >= len(self.nonnes)):
        return 0
      else:
        return self.nonnes[pow]
  def add(self, other):
    maxpow = max(len(self.nonnes), len(other.nonnes))
    minpow = max(len(self.nes),len(other.nes))
    for i in range(len(self.nonnes),maxpow):
      (self.nonnes).append(0)
    for i in range(len(self.nes), minpow):
      (self.nes).append(0)
    for i in range(maxpow):
      self.nonnes[i] = self.nonnes[i] + other.term(i)
    for i in range(minpow):
      self.nes[i] = self.nes[i] + other.term(-(i + 1))
    i = maxpow - 1
    while ((i >= 0) and (self.nonnes[i] == 0)):
      self.nonnes.pop(i)
      i = i - 1
    i = minpow - 1
    while ((i >= 0) and (self.nes[i] == 0)):
      self.nes.pop(i)
      i = i - 1
    return
    
    
  def copy(self):
    new = Poly(0,0)
    new.nes = dcopy(self.nes)
    new.nonnes = dcopy(self.nonnes)
    return new
  def __init__(self, coeff, pow):
    if (pow < 0):
      self.nes = [0]*abs(pow)
      self.nes[-1] = coeff
      self.nonnes = []
    else:
      self.nonnes = [0] * (pow + 1)
      self.nonnes[-1] = coeff
      self.nes = []
    return

  def toString(self):
    strng = ""
    i = len(self.nonnes)-1
    while (i > 0):
      if (self.nonnes[i] > 0):
        strng = strng + " + " + str(self.nonnes[i]) + "y^" + str(i)
      if (self.nonnes[i] < 0):
        strng = strng + " - " + str(-self.nonnes[i]) + "y^" + str(i)
      i = i - 1
    if ((len(self.nonnes)>0) and (self.nonnes[0] > 0)):
      strng = strng + " + " + str(self.nonnes[0])
    if ((len(self.nonnes)>0) and (self.nonnes[0] < 0)):
      strng = strng + " - " + str(self.nonnes[0])
    #i = len(self.nes)-1
    #while (i > 0):
    for i in range(len(self.nes)):
      if (self.nes[i] > 0):
        strng = strng + " + " + str(self.nes[i]) + "y^" + str(-(i+1))
      if (self.nes[i] < 0):
        strng = strng + " - " + str(-self.nes[i]) + "y^" + str(-(i+1))
      #i = i - 1
    if len(strng) == 0:
      return "0"
    newstring = ""
    for i in range(3,len(strng)):
      newstring = newstring + (strng[i])
    if (strng[1] == '-'):
      newstring = '-' + newstring
    return newstring
    
      

def polymult(self, other):
  maxpow = len(self.nonnes) + len(other.nonnes) - 1
  minpow = len(self.nes) + len(other.nes)
  prod = Poly(0,0)
  prod.nes = [0] * minpow
  prod.nonnes = [0] * maxpow
  for i in range(-len(self.nes), len(self.nonnes)):
    for j in range(-len(other.nes), len(other.nonnes)):
      pow = i + j
      if (pow >= 0):
        prod.nonnes[pow] = self.term(i)*other.term(j) + prod.nonnes[pow]
      else:
        prod.nes[-(pow+1)] = prod.nes[-(pow + 1)] + self.term(i) * other.term(j)
  i = minpow - 1
  while ((i >= 0) and (prod.nes[i]==0)):
    prod.nes.pop(i)
    i = i - 1
  i = maxpow - 1
  while ((i >= 0) and (prod.nonnes[i] == 0)):
    prod.nonnes.pop(i)
    i = i - 1
  return prod
  
#checks if two lists have the same elements
#(not necessarily in the same order)
def my_list_equals(list_one, list_two):
  if (len(list_one)!= len(list_two)):
    return False
  for i in list_one:
    if (list_one.count(i) != list_two.count(i)):
      return False
  return True



#The following are the more complex functions




#The critical program that takes in raw notation and computes the SL(3) invariant.
#Tangela uses recursion to compute the polynomial with the skein relation.
#Using helper functions, it creates either scenario in the decomposition,
#computes those polynomials, and adds them together.
#The lower level of recursion deal with the resolution
#of trivalent graphs, all outlined in Frohman(2017).
def Tangela(crossings, threeways, num_strands, strand_ends, strand_overpasses):
  num_strands_two = num_strands
  strand_overpasses_two = dcopy(strand_overpasses)
  strand_overpasses_three = dcopy(strand_overpasses)
  strand_ends_two = dcopy(strand_ends)
  strand_ends_three = dcopy(strand_ends_two)
  crossings_two = dcopy(crossings)
  threeways_three = dcopy(threeways)

  #when all the crossings are resolved
  if (len(crossings) == 0):
    if (len(threeways) == 0):
      mon_a = Poly(1,6)
      mon_a.add(Poly(1,0))
      mon_a.add(Poly(1,-6))
      product = Poly(1,0)
      for i in range(num_strands - 1):
        product = polymult(product,mon_a)
      return product
    bi_info = bi_check(strand_ends,threeways)

    #deals with crushing a bigon
    if (bi_info[0][0] != 0):
      fuse_info = fuseStrings(crossings_two,threeways,bi_info[1][0],bi_info[1][1],strand_ends_two,strand_overpasses_two)
      threeways_two = dcopy(fuse_info[1])
      threeways_two.pop(bi_info[0][1] - 1)
      threeways_two.pop(bi_info[0][0] - 1)
      strand_ends_two = dcopy(fuse_info[2])
      strand_ends_two.pop(bi_info[2][0])
      strand_ends_two.pop(bi_info[2][1])
      strand_overpasses_two = dcopy(fuse_info[3])
      strand_overpasses_two.pop(bi_info[2][0])
      strand_overpasses_two.pop(bi_info[2][1])
      if (bi_info[1][0] == bi_info[1][1]):
        delet = 2
      else:
        delet = 3
      mon_a = Poly(-1,3)
      mon_a.add(Poly(-1,-3))
      return polymult(mon_a,Tangela(crossings_two,threeways_two,num_strands - delet, strand_ends_two, strand_overpasses_two))

    
    quad_info = quad_check(strand_ends_two,threeways)
    #for dealing with quadragons.
    #updates the info accordingly after
    #resolving a quadragon either way
    #there's lot of code here
    #but it's just tedious updating
    #of variables, nothing too fancy.
    #It's just fusing strands together many times.
    if (quad_info[0][0] != 0):
      threeway_info = dcopy(quad_info[0])
      threeway_info.sort()
      threeway_info.reverse()
      threeways_two = dcopy(threeways)
      for j in threeway_info:
        threeways_two.pop(j - 1)
      threeways_three = dcopy(threeways_two)
      strand_overpasses_three = dcopy(strand_overpasses_two)
      strand_ends_three = dcopy(strand_ends_two)
      fuse_info = fuseStrings(crossings_two,threeways_two,quad_info[2][0],quad_info[2][1],strand_ends_two,strand_overpasses_two)
      threeways_two = dcopy(fuse_info[1])
      strand_ends_two = dcopy(fuse_info[2])
      strand_overpasses_two = dcopy(fuse_info[3])
      fuse_info = fuseStrings(crossings_two,threeways_two,quad_info[2][3],quad_info[2][2],strand_ends_two,strand_overpasses_two)
      threeways_two = dcopy(fuse_info[1])
      strand_ends_two = dcopy(fuse_info[2])
      for j in quad_info[1]:
        strand_ends_two.pop(j)
      strand_overpasses_two = dcopy(fuse_info[3])
      fuse_info = Tangela(crossings_two, threeways_two, num_strands - 6, strand_ends_two, strand_overpasses_two)
      fuse_info_two = fuseStrings(crossings_two, threeways_three, quad_info[2][0], quad_info[2][2],strand_ends_three,strand_overpasses_three)
      threeways_three = dcopy(fuse_info_two[1])
      strand_ends_three = dcopy(fuse_info_two[2])
      strand_overpasses_three = dcopy(fuse_info_two[3])
      fuse_info_two = fuseStrings(crossings_two,threeways_three,quad_info[2][3],quad_info[2][1],strand_ends_three,strand_overpasses_three)
      threeways_three = dcopy(fuse_info_two[1])
      strand_ends_three = dcopy(fuse_info_two[2])
      for j in quad_info[1]:
        strand_ends_three.pop(j)
      strand_overpasses_three = dcopy(fuse_info_two[3])
      fuse_info_two = Tangela(crossings_two,threeways_three,num_strands - 6,strand_ends_three,strand_overpasses_three)
      fuse_info_two.add(fuse_info)
      return fuse_info_two
  one_crossing = dcopy(crossings[0])

  #dealing with Reidemeister 1 moves
  #this is solely an optimization
  #to get rid of a crossing without doubling
  #the problem size
  if ((one_crossing[0] == one_crossing[1]) or (one_crossing[0] == one_crossing[2])):
    fuse_info = fuseStrings(crossings,threeways,abs(one_crossing[1]),abs(one_crossing[2]),strand_ends,strand_overpasses_two)
    crossings_two = dcopy(fuse_info[0])
    crossings_two.pop(0)
    threeways_three = dcopy(fuse_info[1])
    strand_overpasses_two = eraseKey(fuse_info[3],abslist(fuse_info[0][0]))
    num_strands_two = num_strands_two - 1
    strand_ends_two = dcopy(fuse_info[2])
    if (one_crossing[1] == one_crossing[2]):
      fuse_info_two = remove_loop(crossings_two,threeways_three,abs(one_crossing[0]),strand_ends_two,strand_overpasses_two)
      crossings_two = dcopy(fuse_info_two[0])
      threeways_three = dcopy(fuse_info_two[1])
      num_strands_two = num_strands_two - fuse_info_two[2] + 1
      strand_ends_two = dcopy(fuse_info_two[3])
      strand_overpasses_two = dcopy(fuse_info_two[4])
    mon_a = Poly(1,(-8)*sign(one_crossing[0]))
    product = polymult(mon_a, Tangela(crossings_two, threeways_three, num_strands_two, strand_ends_two, strand_overpasses_two))
    return product
  

  #dealing with a normal crossing resolution
  #(all other scenarios go here)
  #split open a crossing
  #fuse them into two different arrangements
  #according to the skein, then compute them and add.
  new_strand = max(list(strand_ends_two.keys()))+1
  fuse_info = unfuseCrossing(crossings_two,threeways_three,strand_ends_two,strand_overpasses_two,[abs(one_crossing[1]),abs(one_crossing[2])],abs(one_crossing[0]),new_strand)
  strand_ends_two = dcopy(fuse_info[0])
  strand_overpasses_two = dcopy(fuse_info[1])
  crossings_two = dcopy(fuse_info[2])
  threeways_three = dcopy(fuse_info[3])
  strand_ends_three = dcopy(strand_ends_two)
  strand_overpasses_three = dcopy(strand_overpasses_two)
  threeways_two = dcopy(threeways_three)
  crossings_three = dcopy(crossings_two)
  fuse_info = fuseStrings(crossings_two, threeways_three, new_strand,abs(one_crossing[2]),strand_ends_two,strand_overpasses_two)
  crossings_two = dcopy(fuse_info[0])
  crossings_two.pop(0)
  threeways_three = dcopy(fuse_info[1])
  strand_ends_two = dcopy(fuse_info[2])
  strand_overpasses_two = dcopy(fuse_info[3])
  fuse_info = fuseStrings(crossings_two,threeways_three,abs(one_crossing[1]),abs(one_crossing[0]),strand_ends_two,strand_overpasses_two)
    
  crossings_two = dcopy(fuse_info[0])
  threeways_three = dcopy(fuse_info[1])
  threeways_three.pop(-1)
  threeways_three.pop(-1)
  strand_ends_two = dcopy(fuse_info[2])
  strand_ends_two.pop(new_strand+1)
  strand_overpasses_two = dcopy(fuse_info[3])
  strand_overpasses_two.pop(new_strand+1)
  mon_a = Poly(1,(-2)*sign(one_crossing[0]))
  fuse_info = polymult(mon_a, Tangela(crossings_two,threeways_three,num_strands_two - 1, strand_ends_two, strand_overpasses_two))
  crossings_three.pop(0)
  mon_a = Poly(1,sign(one_crossing[0]))
  new_strand_count = num_strands_two + 2 - strand_ends_three[abs(one_crossing[1])][1].count(abs(one_crossing[0]))
  fuse_info_two = polymult(mon_a, Tangela(crossings_three,threeways_two,new_strand_count, strand_ends_three, strand_overpasses_three))
  fuse_info_two.add(fuse_info)
  return fuse_info_two  

#VERY IMPORTANT: This function's input must have 
#enhanced-Gauss notation.
#Gauss notation by itself is not a unique invariant.
#Using normal Gauss notation will result in a wrong answer.

#Use this function if you have a diagram of a knot/link
#you want to compute.
def slthree_gauss(extended_gauss_notation):
  raw_data = gauss_to_raw(extended_gauss_notation)
  crossings = raw_data[0]
  threeways = []
  num_strands = int(len(flatten(extended_gauss_notation))/2)
  strand_ends = raw_data[1]
  strand_overpasses = raw_data[2]
  answer = Tangela(crossings, threeways, num_strands, strand_ends, strand_overpasses)
  return answer.toString()

#highest-level function. Use this one if
#you are pulling data from KnotInfo.
def slthree_braid(braid):
  if (braid == []):
    return str(1)
  extended_gauss_notation = braid_to_gauss(braid)
  return slthree_gauss(extended_gauss_notation)


#Checks for a bigon (two-sided shape) in the graph.
#It iterates over the set of trivalent vertices.
#If it can pick two edges from that vertex that go to
#another same vertex, we have a bigon.
#bi_check then sends info about that bigon.
def bi_check(strand_ends, threeways):
  threeway_info = [0,0]
  strand_nums_to_join = [0,0]
  tri_list = [[2,3],[1,3],[1,2]]
  for i in range(len(threeways)):
    for tricount in range(3):
      strand_a = abs(threeways[i][tri_list[tricount][0]-1])
      strand_b = abs(threeways[i][tri_list[tricount][1]-1])
      threeway_sign = sign(threeways[i][0])
      source_a = dcopy(strand_ends[strand_a][int((threeway_sign+1)/2)])
      source_b = dcopy(strand_ends[strand_b][int((threeway_sign+1)/2)])
      if (my_list_equals([strand_a] + source_a, [strand_b] + source_b)):
        threeway_info[0] = i + 1
        strand_nums = [min(strand_a, strand_b), max(strand_a, strand_b)]
        strand_nums_to_join[int((threeway_sign+1)/2)] = abs(threeways[i][tricount])
        for j in range(len(threeways)):
          if (threeways[j].count(-threeways[i][tri_list[tricount][0]-1]) == 1):
            threeway_info[1] = j + 1
            for k in range(3):
              if ((abs(threeways[j][k]) == strand_a) or abs(threeways[j][k]) == strand_b):
                m = 1
              else:
                strand_nums_to_join[int((1 - threeway_sign)/2)] = abs(threeways[j][k])
        bi_info = [dcopy(threeway_info),dcopy(strand_nums_to_join),dcopy(strand_nums)]
        #The first part of bi_info is the element numbers in the list
        #of threeway vertices that contain this bigon.
        #The second part is the strand numbers that will
        #be fused together when crushing the bigon.
        #The third part is the strand numbers that will
        #be destroyed.
        return bi_info
  return [[0,0],[0,0]]




#checks for quadragons in the trivalent graph.
#The algorithm iterates over the list of three-edge vertices
#and picks two of the three edges.
#From there, it goes along those edges to two new vertices.
#It checks if there exists an edge from each of those vertices
#that each goes to a same, fourth vertex.
#If that happens, we have traced out a four-sided figure
#and have a quadragon.
#quad_check then returns info about the strands in the quadragon.
def quad_check(strand_ends,threeways):
  threeways_two = abslist(threeways)
  quad_info = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
  tri_list = [[1,2],[0,2],[0,1]]
  for i in range(len(threeways)):
    threeway_sign = sign(threeways[i][0])
    for tricount in range(3):
      threestrand_a = dcopy(strand_ends[threeways_two[i][tri_list[tricount][0]]][int((threeway_sign+1)/2)])
      threestrand_b = dcopy(strand_ends[threeways_two[i][tri_list[tricount][1]]][int((threeway_sign+1)/2)])
      for klink in range(2):
        for klang in range(2):
          far_source_a = dcopy(strand_ends[threestrand_a[klink]][int((1 - threeway_sign)/2)])
          far_source_b = dcopy(strand_ends[threestrand_b[klang]][int((1 - threeway_sign)/2)])
          if (my_list_equals(far_source_a + [threestrand_a[klink]], far_source_b+[threestrand_b[klang]])):
            quad_info[1][2] = threestrand_a[klink]
            quad_info[1][3] = threestrand_b[klang]
            quad_info[1][0] = threeways_two[i][tri_list[tricount][0]]
            quad_info[1][1] = threeways_two[i][tri_list[tricount][1]]
            if (threeway_sign == -1):
              quad_info[2][0] = threeways_two[i][tricount]
              quad_info[2][1] = threestrand_a[1 - klink]
              quad_info[2][2] = threestrand_b[1 - klang]
              for j in range(2):
                if (far_source_a[j] != threestrand_b[klang]):
                  quad_info[2][3] = far_source_a[j]
            else:
              quad_info[2][2] = threeways_two[i][tricount]
              quad_info[2][0] = threestrand_a[1 - klink]
              quad_info[2][3] = threestrand_b[1 - klang]
              for j in range(2):
                if (far_source_a[j] != threestrand_b[klang]):
                  quad_info[2][1] = far_source_a[j]
            quad_info[0][0] = i+1
            for j in range(len(threeways)):
              if (threeways[j].count(threestrand_a[klink]*(-1)*threeway_sign) == 1):
                quad_info[0][1] = j+1
              if (threeways[j].count(threestrand_b[klang]*(-1)*threeway_sign) == 1):
                quad_info[0][2] = j+1
              if (threeways[j].count(threestrand_b[klang]*threeway_sign) == 1):
                quad_info[0][3] = j+1
            #quad_info has three parts
            #1. The element numbers in the list of tri-vertices that contains the quadragon.
            #2. The strand numbers of the quadragon edges.
            #3. The strand numbers outside of the quadragon (to be joined).
            return dcopy(quad_info);

#function is called when a crossing is erased. It erases
#the crossing's info from the overpass list.
def eraseKey(strand_overpasses,to_erase):
  overstrand = to_erase[0]
  strand_overpasses_two = dcopy(strand_overpasses)
  overstrand_overpasses = strand_overpasses[overstrand]
  for i in range(len(overstrand_overpasses)):
    if (overstrand_overpasses[i] == [to_erase[1],to_erase[2]]):
      overstrand_overpasses_two = dcopy(overstrand_overpasses)
      overstrand_overpasses_two.pop(i)
      strand_overpasses_two[overstrand] = dcopy(overstrand_overpasses_two)
      return strand_overpasses_two



def remove_loop(crossings,threeways,strand_num,strand_ends,strand_overpasses):
  threeways_two = dcopy(threeways)
  num_strands = 0
  crossings_two = dcopy(crossings)
  strand_overpasses_two = dcopy(strand_overpasses)
  strand_ends_two = dcopy(strand_ends)
  i = len(crossings)
  while (i >= 1):
    i = i - 1
    if ((abs(crossings_two[i][0]) == strand_num) and (abs(crossings_two[i][1]) != strand_num) and (abs(crossings_two[i][2]) != strand_num)):
      fuse_info = fuseStrings(crossings_two,threeways_two,abs(crossings_two[i][2]),abs(crossings_two[i][1]),strand_ends_two,strand_overpasses_two)
      crossings_two = dcopy(fuse_info[0])
      threeways_two = dcopy(fuse_info[1])
      strand_ends_two = dcopy(fuse_info[2])
      strand_overpasses_two = dcopy(fuse_info[3])
      num_strands = num_strands + 1
      strand_overpasses_two.pop(strand_num)
      strand_ends_two.pop(strand_num)
      crossings_two.pop(strand_num)
  return [crossings_two,threeways_two,num_strands,strand_ends_two,strand_overpasses_two]

#This takes two strands and fuses them together.
#By fusing them together, the list of crossings is updated,
#as well as the list of strand ends. The list of overpasses for
#the two fused strands is merged.
def fuseStrings(crossings, threeways, ending_strand, joining_strand, strand_ends, strand_overpasses):
  crossings_two = dcopy(crossings)
  strand_overpasses_two = dcopy(strand_overpasses)
  strand_ends_two = dcopy(strand_ends)
  threeways_two = dcopy(threeways)
  check = 0
  if (joining_strand != ending_strand):
    end_key_list = list(strand_ends.keys())
    if (end_key_list.count(joining_strand) == 0):
      strand_overpasses_two[joining_strand] = []
      check = 1
    for i in range(len(crossings_two)):
      for j in range(3):
        if (abs(crossings_two[i][j]) == ending_strand):
          crossings_two[i][j] = joining_strand*sign(crossings_two[i][j])
    for i in range(len(end_key_list)):
      one_string_end = strand_ends_two[end_key_list[i]]
      for k in range(2):
        for j in range(len(one_string_end[k])):
          if (abs(one_string_end[k][j])==ending_strand):
            one_string_end[k][j] = joining_strand*sign(one_string_end[k][j])
      strand_ends_two[end_key_list[i]] = one_string_end
    for i in range(len(threeways_two)):
      for j in range(3):
        if (abs(threeways_two[i][j]) == ending_strand):
          threeways_two[i][j] = joining_strand*sign(threeways_two[i][j])
    end_key_list = list(strand_overpasses_two.keys())
    for i in range(len(end_key_list)):
      one_string_end = strand_overpasses_two[end_key_list[i]]
      for k in range(len(one_string_end)):
        for j in range(len(one_string_end[k])):
          if (one_string_end[k][j] == ending_strand):
            one_string_end[k][j] = joining_strand
      strand_overpasses_two[end_key_list[i]] = one_string_end
    strand_overpasses_two[joining_strand] = strand_overpasses_two[ending_strand] + strand_overpasses_two[joining_strand]
  if (check == 1):
    strand_ends_two[joining_strand] = strand_ends_two[ending_strand]
  else:
    strand_ends_two[joining_strand] = [strand_ends_two[ending_strand][0],strand_ends_two[joining_strand][1]]
  if (joining_strand != ending_strand):
    strand_ends_two.pop(ending_strand)
    strand_overpasses_two.pop(ending_strand)
  return [crossings_two, threeways_two,strand_ends_two,strand_overpasses_two]

#takes a crossing and splits it into four strands
#this prepares the area for two different resolutions
#as per the skein relation outlined in Frohman (2017)
def unfuseCrossing(crossings, threeways, strand_ends, strand_overpasses, understrands, overstrand, breakaway_strand):
  end_key_list = dcopy(list(strand_ends.keys()))
  strand_overpasses_two = dcopy(strand_overpasses)
  hoopa = max(end_key_list) + 2
  strand_ends_two = dcopy(strand_ends)
  crossings_two = dcopy(crossings)
  threeways_two = dcopy(threeways)
  overstrand_overpasses = dcopy(strand_overpasses[overstrand])
  tri_list = [[1,2],[0,2],[0,1]]
  #overpasses_cache keeps the data that would otherwise
  #be lost when we pop entries from overstrand_overpasses
  overpasses_cache = []
  num_overstrand_overpasses = len(overstrand_overpasses)
  for i in range(num_overstrand_overpasses):
    overstrand_overpass_iter = overstrand_overpasses[0]
    if (overstrand_overpass_iter == understrands):
      overstrand_overpasses.pop(0)
      strand_overpasses_two[overstrand] = dcopy(overstrand_overpasses)
      strand_overpasses_two[breakaway_strand] = dcopy(overpasses_cache)
      strand_ends_two[understrands[0]] = [strand_ends_two[understrands[0]][0]]+[[breakaway_strand,hoopa]]
      strand_ends_two[understrands[1]] = [[overstrand,hoopa]]+[strand_ends_two[understrands[1]][1]]
      strand_ends_two[breakaway_strand] = [strand_ends[overstrand][0]]+[[understrands[0],hoopa]]
      strand_ends_two[overstrand] = [[hoopa,understrands[1]], strand_ends[overstrand][1]]
      strand_ends_two[hoopa] = [[overstrand,understrands[1]],[breakaway_strand, understrands[0]]]
      strand_overpasses_two[hoopa] = []
      breakaway_strand_begin = dcopy(strand_ends_two[breakaway_strand][0])
      check = 1
      for j in range(len(crossings_two)):
        if (abs(crossings_two[j][2]) == overstrand):
          check = 2
          crossings_two[j][2] = breakaway_strand*sign(crossings_two[j][0])
          strand_ends_two[abs(crossings_two[j][1])] = [strand_ends_two[abs(crossings_two[j][1])][0]] + [[abs(crossings_two[j][0]),breakaway_strand]]
          #other_overpasses is complex here.
          #After finding the crossing where your overstrand
          #ends, we take the overstrand of that crossing
          #and take the list of all its overpasses.
          pora = dcopy(strand_overpasses_two[abs(crossings_two[j][0])])
          for pory in range(len(pora)):
            if (pora[pory][1] == overstrand):
              pora[pory][1] = breakaway_strand
          strand_overpasses_two[abs(crossings_two[j][0])] = dcopy(pora)
      if (check == 1):
        for j in range(len(threeways_two)):
          if ((my_list_equals(breakaway_strand_begin+[overstrand], abslist(threeways_two[j]))) and (sign(threeways_two[j][0]) == 1)):
            for pory in range(3):
              if (threeways_two[j][pory] == overstrand):
                threeways_two[j][pory] = breakaway_strand
            for pory in range(3):           
              strand_ends_two[threeways_two[j][pory]] = [[threeways_two[j][tri_list[pory][0]],threeways_two[j][tri_list[pory][1]]]]+ [dcopy(strand_ends_two[threeways_two[j][pory]][1])]
      for j in range(len(overpasses_cache)):
        for m in range(len(crossings_two)):
          if ((abs(crossings_two[m][0]) == overstrand) and (abs(crossings_two[m][1]) == overpasses_cache[j][0])):
            crossings_two[m][0] = breakaway_strand*sign(crossings_two[m][0])
        if (overpasses_cache[j][0] == overpasses_cache[j][1]):
          strand_ends_two[overpasses_cache[j][1]] = [[breakaway_strand,overpasses_cache[j][1]],[breakaway_strand,overpasses_cache[j][1]]]
        else:
          strand_ends_two[overpasses_cache[j][0]] = [strand_ends_two[overpasses_cache[j][0][0]]]+[[breakaway_strand,overpasses_cache[j][1]]]
          strand_ends_two[overpasses_cache[j][1]] = [[breakaway_strand,overpasses_cache[j][0]]]+[strand_ends_two[overpasses_cache[j][1]][1]]
      overpasses_cache = dcopy(strand_ends_two[breakaway_strand][0])
      overstrand_overpasses = dcopy(strand_overpasses_two[overpasses_cache[0]])
      for j in range(len(overstrand_overpasses)):
        if ((overstrand_overpasses[j][0] == overpasses_cache[1]) and (overstrand_overpasses[j][1] == overstrand)):
          overstrand_overpasses[j] = [overpasses_cache[1],breakaway_strand]
      strand_overpasses_two[overpasses_cache[0]] = dcopy(overstrand_overpasses)
      threeways_two.append([-breakaway_strand,-understrands[0],-hoopa])    
      threeways_two.append([overstrand,understrands[1],hoopa])
      return [dcopy(strand_ends_two),dcopy(strand_overpasses_two),dcopy(crossings_two),dcopy(threeways_two)]
    overpasses_cache.append(overstrand_overpass_iter)
    overstrand_overpasses.pop(0)

            
#Converts extended Gauss notation to raw notation that will be fed to Tangela     
#The function gets three main things from the Gauss notation:
#1. Crossings info. With each crossing, it converts it to strand data.
#2. Strand end info. With each crossing, it checks
#   the understrands to see which crossings a strand
#   begins and ends at.
#3. Strand overpasses. With each crossing, it checks the overstrand
# to keep track of the crossings a strand goes over.
def gauss_to_raw(gauss):
  if (flatten(gauss) == gauss):
    gauss_two = [gauss]
    return gauss_to_raw(gauss_two)
  num_crossings = int(len(flatten(gauss))/2)
  strand_num = 1
  proto_crossings = make_twolist(0,3,num_crossings)
  proto_strand_ends = []
  proto_strand_overpasses = []
  one_proto_overpass = []
  checklist = [0]*num_crossings
  minor_list = dcopy(checklist)
  one_proto_strand = [0,0]
  understrand_num = 1
  for i in range(len(gauss)):
    component = gauss[i]
    num_crossings_comp = int(len(component)/2)
    for j in range(2*num_crossings_comp):
      if (checklist[abs(component[j]) - 1] == 0):
        checklist[abs(component[j]) - 1] = checklist[abs(component[j]) - 1] + 1
        minor_list[abs(component[j]) - 1] = sign(component[j])
        if (component[j] > 0):
          proto_crossings[abs(component[j]) - 1][0] = strand_num
          one_proto_overpass = one_proto_overpass + [abs(component[j])]
        else:
          proto_crossings[abs(component[j]) - 1][1] = strand_num
          one_proto_strand[1] = abs(component[j])
          strand_num = strand_num + 1
          proto_crossings[abs(component[j]) - 1][2] = strand_num
          proto_strand_ends = proto_strand_ends + [one_proto_strand]
          one_proto_strand = [abs(component[j]), 0]
          proto_strand_overpasses = proto_strand_overpasses + [one_proto_overpass]
          one_proto_overpass = []
          k = abs(component[j])
      else:
        strand_num_three = abs(component[j])
        ##426
        if (minor_list[strand_num_three - 1] < 0):
          proto_crossings[strand_num_three - 1][0] = strand_num
          one_proto_overpass = one_proto_overpass + [strand_num_three]
        else:
          proto_crossings[strand_num_three - 1][1] = strand_num
          one_proto_strand[1] = strand_num_three
          strand_num = strand_num + 1
          proto_crossings[strand_num_three - 1][2] = strand_num
          k = strand_num_three
          proto_strand_ends = proto_strand_ends + [one_proto_strand]
          one_proto_strand = [strand_num_three, 0]
          proto_strand_overpasses = proto_strand_overpasses + [one_proto_overpass]
          one_proto_overpass = []
        proto_crossings[strand_num_three - 1] = listmult(proto_crossings[strand_num_three - 1],sign(component[j]))
    proto_crossings[k - 1][2] = sign(proto_crossings[k - 1][1])*understrand_num
    proto_strand_overpasses[understrand_num - 1] = one_proto_overpass + proto_strand_overpasses[understrand_num - 1]
    for j in range(len(one_proto_overpass)):
      proto_crossings[one_proto_overpass[j] - 1][0] = understrand_num * sign(proto_crossings[one_proto_overpass[j] - 1][0])
    proto_strand_ends[understrand_num - 1][0] = k
    understrand_num = strand_num
    one_proto_overpass = []
  #442
  crossings = proto_crossings
  strand_ends = {}
  for j in range(num_crossings):
    strand_ends[j+1] = [[abs(proto_crossings[proto_strand_ends[j][0] - 1][0]), abs(proto_crossings[proto_strand_ends[j][0] - 1][1])], [abs(proto_crossings[proto_strand_ends[j][1] - 1][0]), abs(proto_crossings[proto_strand_ends[j][1] - 1][2])]]
  strand_overpasses = {}
  for j in range(num_crossings):
    minor_list = proto_strand_overpasses[j]
    for k in range(len(minor_list)):
      minor_list[k] = [abs(proto_crossings[minor_list[k] - 1][1]),abs(proto_crossings[minor_list[k] - 1][2])]
    strand_overpasses[j+1] = minor_list
  return [crossings,strand_ends, strand_overpasses]
      
          
  



##463
#converts braid notation to extended Gauss notation.
#It does this by starting at strand 1 of the braid.
#As it hits a relevant crossing, the current strand
#it is on will be updated to go one up or down.
#While this is happening, each crossing adds information
#to the Gauss notation. (We also keep a list
#indicating if a crossing has been visited before,
#as this affects the Gauss notation.)
#When we reach the end of the braid,
#we start over on that same strand.
#We does this until all braid strands have been
#tried.
def braid_to_gauss(braid):
  braid_length = len(braid)
  if (braid_length == 2):
    if (type(braid[1]) == list):
      if (len(braid[1]) != 0):
        return braid_to_gauss(braid[1])
  abs_braid = abslist(braid)
  strand_checklist = [0]*(max(abs_braid)+1)
  proto_gauss_part = {}
  strand_checklist[0] = 1
  braid_strand = 1
  gauss = []
  gauss_part = []
  gauss_crossing = 1
  #visited keeps track of whether we've already checked
  #the crossing in braid notation (changes how it's
  #written in Gauss notation)
  visited = [0]*braid_length
  while (min(strand_checklist) == 0):
    strand_checklist[braid_strand - 1] = 1
    for i in range(braid_length):
      if (abs_braid[i] == braid_strand):
        if (visited[i] == 0):
          visited[i] = 1
          proto_gauss_part[i] = gauss_crossing
          gauss_part.append(-sign(braid[i])*gauss_crossing)
          gauss_crossing = gauss_crossing + 1
        else:
          visited[i] = 2
          gauss_part.append(proto_gauss_part[i]*sign(braid[i]))
        braid_strand = braid_strand + 1
      else:
        if (abs_braid[i] == braid_strand - 1):
          if (visited[i] == 0):
            visited[i] = 1
            proto_gauss_part[i] = gauss_crossing
            gauss_part.append(sign(braid[i])*gauss_crossing)
            gauss_crossing = gauss_crossing + 1
          else:
            visited[i] = 2
            gauss_part.append(proto_gauss_part[i]*sign(braid[i]))
          braid_strand = braid_strand - 1
    if (strand_checklist[braid_strand - 1] == 1):
      gauss.append(gauss_part)
      j = 1
      while ((j <= len(strand_checklist)) and (strand_checklist[j-1] == 1)):
        j = j + 1
      braid_strand = j
      gauss_part = []
  if (len(gauss) == 1):
    gauss = flatten(gauss)
  return gauss
