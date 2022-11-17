from nadia_pt_fo import check_proof

print(check_proof('''1. A|B              pre
2. A->C             pre
3. B->C             pre
4. {    A           hip
5.      C           ->e 4,2
   } 
6. {    B           hip
7.      C           ->e 6,3
   }
8. C                |e 1, 4-5, 6-7'''))