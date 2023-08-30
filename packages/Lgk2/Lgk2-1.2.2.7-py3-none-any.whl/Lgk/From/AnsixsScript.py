class Remove:
   @staticmethod
   def Es(user_input):
      cleaned_input = ' '.join(user_input.split())
      return cleaned_input
   
   def Word(args, w):
       args = args.replace(w, "")
       return args

class Take:
   def First_Word(args):
      v = ""
      for i in range(len(args)):
         if args[i] == " ":
            break
         else:
            v += args[i]
      return v
   #Take word from under a, b
   def Under(a,b,*args):
      text = ''.join(args)
      result = ''
      i = 0
      while i < len(text):
          if text[i] == a:
              i += 1
              while i < len(text):
                  if text[i] == b:
                      break
                  result += text[i]
                  i += 1
          else:
              i += 1
      return result

class show:
   def direct(value, conditions):
      pas = ""
      sep1 = conditions.split(",")
      c = conditions.count(",")
      for i in range(c+1):
         sep2 = sep1[i].split("=")
         if sep2[0] == value:
            if sep2[1] == "pass":
               pas += "pass"
            else:
               pas += "pass"
               print(sep2[1],flush=True)
      if pas == "pass":
         pass
      else:
         print(value,flush=True)

   def _return(value, conditions):
      pas = ""
      sep1 = conditions.split(",")
      c = conditions.count(",")
      for i in range(c+1):
         sep2 = sep1[i].split("=")
         if sep2[0] == value:
            if sep2[1] == "pass":
               pas += "pass"
            else:
               pas += "pass"
               return(sep2[1])
      if pas == "pass":
         pass
      else:
         return(value)

class shorc:
   class clear:
      def screen():
         import os
         os.system("clear")

   def reanes(args, v):
      args = str(args)
      args = args.replace(v, '')
      args = Remove.Es(args)
      return args

def spots(spot, items, relate):
   main = []
   spv = spot.split("&")
   i = items.split("&")
   v = 0
   try:
      for j in i:
         if relate == j:
            sp2 = spv[v]
            sp2 = sp2.replace("['", '')
            sp2 = sp2.replace("']", "")
            sp2 = sp2.split("', '")
            for g in sp2:
               main.append(g)
      v += 1
   except:
       pass
   return main