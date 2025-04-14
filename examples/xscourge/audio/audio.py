from xddtools.entries.bank import BankExtractor


if __name__ == '__main__':
    extractor = BankExtractor()
    extractor.extract("hero_Scourge.bank", "./")
