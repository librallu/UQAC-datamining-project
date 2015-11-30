import sys


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("mauvais nombre d'arguments.")
	else:
		# argument reading
		input_name = sys.argv[1]
		output_name = sys.argv[2]
		f_in = open(input_name, 'r')
		
		# read the field name from csv
		fields = f_in.readline().replace('\n', '')
		fields = fields.split('\t')
			
		order = [
			"nutrition-score-fr_100g",
			"energy_100g",
			"fat_100g",
			"saturated-fat_100g",
			"carbohydrates_100g",
			"sugars_100g",
			"fiber_100g",
			"proteins_100g",
			"salt_100g",
			"sodium_100g",
			"vitamin-c_100g"
		]
		
		# for weka, the first attribute is the last on the list
		order.reverse()
			
		# keep information about the type of each field
		field_action = {}
		for i in order:
			field_action[i] = "numeric"
		field_action["nutrition-score-fr_100g"] = "discrete"

		
		#~ for i,v in enumerate(fields):
			#~ if field_action[i] != "discard":
				#~ print('"'+v+'",')
		
		# lines ( dict array)
		# dict contains as key the field name 
		# and as value the associated value.
		lines = []
		nb_missed = 0
		for l in f_in.readlines():
			l.replace('\n', '')
			l = l.split('\t')
			tmp_line = {}
			missed=False
			for i,f in enumerate(fields):
				if f in order:
					if f == "nutrition-score-fr_100g" and l[i]:
						l[i] = int(l[i])
						if l[i] < 0 :
							l[i] = 'bad'
						elif l[i] < 10:
							l[i] = 'medium'
						else:
							l[i] = 'good'
					if l[i]:
						tmp_line[f] = l[i]
					else:
						tmp_line[f] = '?'
						missed=True
			if not missed:
				lines.append(tmp_line)
			else:
				nb_missed += 1

		print("nb missed: {}".format(nb_missed))
		f_in.close()
		
		header = ''
		header += '@relation foodfacts\n'
		for i in order:
			if field_action[i] == "numeric":
				header += '@attribute {} numeric\n'.format(i)
			else:
				header += '@attribute {} {}\n'.format(i, "{bad, medium, good}")
		header += '@data\n'
		
		#~ print(header)
		
		# writing file
		output_file = open(output_name, 'w')
		output_file.write(header+'\n')
		
		# adding content
		for l in lines:
			#~ print(','.join([l[f] for f in order ]))
			output_file.write(','.join([l[f] for f in order ])+'\n')
			
		output_file.close()
		
		
		# compute information about the number of filled fields
		#~ field_info = {}
		#~ for l in lines:
			#~ nb = 0
			#~ for e in l:
				#~ if l[e]:
					#~ nb += 1
			#~ if field_info.has_key(nb):
				#~ field_info[nb] += 1
			#~ else:
				#~ field_info[nb] = 1
		#~ for k in field_info:
			#~ print('{} -> {}'.format(k, field_info[k]))
		
		
		
	
	
