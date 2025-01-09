from database import get_data
def authentication(*data):
	print(data)
	if len(data) == 3 and data[1] != data[2]:
		return "Two password not match"
	if len(data) == 2:
		return "Username Password incorrect"
	return f"Hello {data[0]}"

def check_password(username, password):
	data = get_data("users")
	
	for row in data:
		if row[1] == username and row[2] == password:
			return True
	return False
	
if __name__ == "__main__":
	# test code
	#temp = authentication("Adi", "abcd", "abce")
	#temp = authentication("Adi", "abce")
	#print(temp)
	print(check_password("Adi","1234"))
	print(check_password("Adi","aaaa"))
	print(check_password("Ali","aaaa"))
