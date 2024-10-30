import re


class EmailMasker:
    '''Класс для экранирования почтового адреса'''

    def __init__(self, mask_char="x"):
        self.mask_char = mask_char

    def mask_email(self, email):
        parts = email.split("@")
        if len(parts) == 2:
            local_part = parts[0]
            domain = parts[1]
            masked_local_part = self.mask_char * len(local_part)
            return f"{masked_local_part}@{domain}"
        else:
            raise ValueError("Invalid email format")

a_1 = EmailMasker("x")
print(a_1.mask_email("aaaa@aaa.com")) # -> xxxx@aaa.com


class PhoneNumberMasker:
    '''Класс для экранирования номера телефона'''

    def __init__(self, mask_char="x", num_chars_to_mask=3):
        self.mask_char = mask_char
        self.num_chars_to_mask = num_chars_to_mask

    def mask_phone_number(self, phone_number):
        parts = phone_number.split()
        answer = []
        a = 0
        for part in parts[::-1]:
            s = []
            for symbol in part[::-1]:
                if a == self.num_chars_to_mask:
                    s.append(symbol)
                else:
                    s.append(self.mask_char)
                    a+=1
            answer.append("".join(s[::-1]))
        return " ".join(answer[::-1])

a_2 = PhoneNumberMasker("x", 4)
print(a_2.mask_phone_number("+7 666 777       888")) # -> +7 666 77x xxx


class SkypeMasker:
    '''Класс для экранирования ссылок skype'''

    def __init__(self, mask_char="x"):
        self.mask_char = mask_char

    def mask_skype(self, string):
        pattern = r"skype:[\w.]+"
        replacement = f"skype:{3 * self.mask_char}"

        return re.sub(pattern, replacement, string)

a_3 = SkypeMasker("x")
print(a_3.mask_skype("skype:alex.max")) # -> skype:xxx
print(a_3.mask_skype("<a href=\"skype:alex.max?call\">skype</a>")) # -> <a href="skype:xxx?call">skype</a>