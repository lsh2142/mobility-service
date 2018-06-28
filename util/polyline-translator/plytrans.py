def main():
    encode = raw_input("Please enter the whole polyline: ")
    startX = raw_input("Start Lat: ")
    startY = raw_input("Start Lng: ")
    endX = raw_input("End Lat: ")
    endY = raw_input("End Lng: ")

    index = 0
    chunk = 0
    isLat = True
    foundStart = False
    writeSnippet = False

    start = {}
    end = {}
    start["lat"] = float(startX)
    start["lng"] = float(startY)
    end["lat"] = float(endX)
    end["lng"] = float(endY)

    geo = {}
    geo["lat"] = 0.0
    geo["lng"] = 0.0

    code = {}
    snippet = ""

    while(True):
        result = 0
        shift  = 0
        ret    = 0
        code["original"] = ""
        code["literal"]  = ""
        code["binary"]   = ""

        print("--- Code chunk " + str(chunk) + " ---")

        while(True):
            orgdec = ord(encode[index]) - 63
            index += 1

            result |= (orgdec & 0x1f) << shift
            shift += 5

            code["original"] += chr(orgdec + 63) + ""
            code["literal"] += str(orgdec) + " "
            code["binary"]  += str(bin(orgdec)) + " "

            if(orgdec < 0x20):
                break

            if(index >= len(encode)):
                break

        if(result&1 != 0):
            result = ~(result >> 1)
        else:
            result = result >> 1

        ret = result / 1E5

        if(writeSnippet):
            snippet += code["original"]

        if(isLat):
            print("Type: Latitude")
            geo["lat"] += ret
            isLat = False
        else:
            print("Type: Longitude")
            geo["lng"] += ret
            print("LatLng obtained : " + str(geo["lat"]) + ", " + str(geo["lng"]))

            if((foundStart == False) and str(geo["lat"]) == str(start["lat"]) and str(geo["lng"]) == str(start["lng"])):
                foundStart = True
                writeSnippet = True
                snippet += encode_latlng(start["lat"], start["lng"])
            elif(foundStart == True and str(geo["lat"]) == str(end["lat"]) and str(geo["lng"]) == str(end["lng"])):
                writeSnippet = False
                print("Found endpoint!")

            isLat = True
        
        print("Code: " + code["original"])
        print("Literal: " + code["literal"])
        print("Binary: " + code["binary"])
        print("Value: " + str(ret))

        print("--- End code chunk " + str(chunk) + " ---")
        chunk += 1

        if(index >= len(encode)):
            break

    print("Found snippet: " + snippet)


def encode_latlng(lat, lng):
    a = "test"
    print("Lets encode!")
    return a

if __name__ == "__main__":
    main()
