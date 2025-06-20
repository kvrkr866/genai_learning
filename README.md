# genai_learning
Gen AI Learning

The implemented AI based Assistant for Trip Planner was a small attempt towards Agentic world of AI. 
# What was implemented:
> Langgraph based Agentic flow (parallel, merge, utility functions and graph flow was done).
> Web search Tools used were - DuckDuckGo, Tavily
> LLM Models used were - Groq, Anthropic
> weather search, currency exchange rate purpose third party REST API used with the help of requests.
> Modulerized code implemented.
> Some utility functions were also implemented. In future these can be moved to another file.
> All the requirements were addressed at high level.
>
# TODO Activities:
1. proper deployment of tool(s) and well defined control for tools invocation (tool sake implemented but do not want to give the control to LLM, hence removed)
2. conditional edges were implemnted but it was not necessary hence removed (code moved to commented section)
3. Some optimization in cost summarization and consolidated report needed.
4. Implmented chatGPT, google Gemini feedback on the code. Need to further review for better code.
5. Need to make it more modularized for llm passing, do init once and use many times kind of approach. At present many places creating, using and destroying. In long run this may lead to lot of latency and resource challenges.


# The output of the first version is as follows :
## User Input: I am from Bengaluru, India. I would like to go for a trip to Bali, Indonesia from 25th June to 30th June. Give me trip planner along with cost in INR.

# the output from AI Trip Planner Assistant was follows for the above input:
------------------------------------------------------------------------------------------
### Final Report on Trip Plan ###

    **Attractions & Itinerary:**
    Planning a 6-day trip to Bali, Indonesia, from June 25th to June 30th, is an exciting endeavor! Bali is known for its beautiful beaches, lush green landscapes, vibrant culture, and delicious cuisine. Below is a detailed trip planner, including attractions, activities, famous 
festivals, restaurants, and local transportation options. I've also included approximate costs to help you plan your trip better.

---

### **Day 1: Arrival in Bali and Exploring South Bali**
**Date:** June 25th
**Focus:** Arrival and relaxation

#### **Morning:**
- **Arrival in Bali:** Land at Ngurah Rai International Airport (DPS) in Denpasar.
- **Transfer to Hotel:** Hire a taxi or use a ride-hailing app like Grab or Gojek to reach your hotel in South Bali (e.g., Kuta, Seminyak, or Canggu). Cost: ~INR 1,200 - 1,500 (IDR 25,000 - 30,000).
- **Check-in:** Stay in a budget-friendly hotel or guesthouse. Cost: ~INR 2,000 - 3,000 per night (IDR 40,000 - 60,000).

#### **Afternoon:**
- **Lunch:** Visit a local warung (food stall) for authentic Balinese dishes like Nasi Goreng or Babi Guling. Cost: ~INR 300 - 500 (IDR 6,000 - 10,000).
- **Visit Uluwatu Temple:** Explore this stunning Balinese Hindu temple perched on a cliff. Entrance fee: ~INR 500 (IDR 10,000).
- **Relax at Padang Padang Beach or Seminyak Beach:** Enjoy the sunset at one of Bali's most beautiful beaches.

#### **Evening:**
- **Dinner:** Head to Jimbaran Bay for a seafood dinner on the beach. Cost: ~INR 800 - 1,200 (IDR 15,000 - 25,000).
- **Night Walk:** Stroll around Kuta or Seminyak for some shopping or nightlife.

**Day 1 Cost Estimate:** ~INR 6,000 - 8,000 (IDR 120,000 - 160,000).

---

### **Day 2: Ubud and Surroundings**
**Date:** June 26th
**Focus:** Culture, nature, and art

#### **Morning:**
- **Breakfast:** Enjoy a traditional Balinese breakfast at your hotel. Cost: ~INR 300 (IDR 6,000).
- **Tegallalang Rice Terraces:** Visit the iconic rice fields. Entrance fee: ~INR 500 (IDR 10,000).
- **Tirta Empul Temple:** Explore this sacred water temple. Entrance fee: ~INR 500 (IDR 10,000).

#### **Afternoon:**
- **Lunch:** Dine at a local warung near Ubud. Cost: ~INR 300 - 500 (IDR 6,000 - 10,000).
- **Sacred Monkey Forest Sanctuary:** Walk through the forest and see the Balinese long-tailed macaques. Entrance fee: ~INR 600 (IDR 12,000).
- **Ubud Royal Palace:** Learn about Balinese history and culture. Entrance fee: ~INR 300 (IDR 6,000).

#### **Evening:**
- **Dinner:** Try traditional Balinese cuisine at a local restaurant like Bebek Bengil (Duck Restaurant). Cost: ~INR 800 - 1,200 (IDR 15,000 - 25,000).
- **Cultural Performance:** Watch a traditional Balinese dance performance (e.g., Legong or Kecak). Ticket: ~INR 500 - 800 (IDR 10,000 - 15,000).

**Day 2 Cost Estimate:** ~INR 5,000 - 7,000 (IDR 100,000 - 140,000).

---

### **Day 3: East Bali (Tirta Gangga and Lempuyang)**
**Date:** June 27th
**Focus:** Nature and scenic views

#### **Morning:**
- **Breakfast:** Enjoy a hearty breakfast at your hotel. Cost: ~INR 300 (IDR 6,000).
- **Tirta Gangga Water Palace:** Explore this beautiful water garden. Entrance fee: ~INR 300 (IDR 6,000).
- **Lempuyang Temple:** Visit the famous "Gates of Heaven" for stunning views. Entrance fee: ~INR 500 (IDR 10,000).

#### **Afternoon:**
- **Lunch:** Dine at a local restaurant near Tirta Gangga. Cost: ~INR 300 - 500 (IDR 6,000 - 10,000).
- **Taman Ujung Water Palace:** Another beautiful water palace with great photo opportunities. Entrance fee: ~INR 300 (IDR 6,000).

#### **Evening:**
- **Dinner:** Head back to your hotel or visit a nearby beach like Candidasa Beach for a seafood dinner. Cost: ~INR 800 - 1,200 (IDR 15,000 
- 25,000).

**Day 3 Cost Estimate:** ~INR 4,500 - 6,500 (IDR 90,000 - 130,000).

---

### **Day 4: Nusa Penida Day Trip**
**Date:** June 28th
**Focus:** Adventure and beaches

#### **Morning:**
- **Breakfast:** Early breakfast at your hotel. Cost: ~INR 300 (IDR 6,000).
- **Fast Boat to Nusa Penida:** Take a fast boat from Sanur to Nusa Penida. Cost: ~INR 2,000 - 3,000 (IDR 40,000 - 60,000).
- **Kelingking Beach:** Visit this iconic beach with a unique limestone cliff. Entrance fee: ~INR 500 (IDR 10,000).

#### **Afternoon:**
- **Lunch:** Eat at a local warung on Nusa Penida. Cost: ~INR 300 - 500 (IDR 6,000 - 10,000).
- **Angel’s Billabong:** Explore this natural infinity pool. Entrance fee: ~INR 300 (IDR 6,000).
- **Crystal Bay:** Relax at this stunning beach with crystal-clear water. Entrance fee: ~INR 300 (IDR 6,000).

#### **Evening:**
- **Return to Bali:** Take the fast boat back to Sanur. Cost: ~INR 2,000 - 3,000 (IDR 40,000 - 60,000).
- **Dinner:** Dine at a restaurant in Sanur. Cost: ~INR 800 - 1,200 (IDR 15,000 - 25,000).

**Day 4 Cost Estimate:** ~INR 6,500 - 8,500 (IDR 130,000 - 170,000).

---

### **Day 5: North Bali (Tanah Lot and Jatiluwih)**
**Date:** June 29th
**Focus:** Scenic landscapes and temples

#### **Morning:**
- **Breakfast:** Enjoy breakfast at your hotel. Cost: ~INR 300 (IDR 6,000).
- **Tanah Lot Temple:** Visit this iconic sea temple. Entrance fee: ~INR 500 (IDR 10,000).

#### **Afternoon:**
- **Lunch:** Dine at a local restaurant near Tanah Lot. Cost: ~INR 300 - 500 (IDR 6,000 - 10,000).
- **Jatiluwih Rice Terraces:** Explore the UNESCO-listed rice fields. Entrance fee: ~INR 500 (IDR 10,000).

#### **Evening:**
- **Dinner:** Head to Canggu or Echo Beach for a sunset dinner. Cost: ~INR 800 - 1,200 (IDR 15,000 - 25,000).

**Day 5 Cost Estimate:** ~INR 4,500 - 6,500 (IDR 90,000 - 130,000).

---

### **Day 6: Departure**
**Date:** June 30th
**Focus:** Last-minute shopping and departure

#### **Morning:**
- **Breakfast:** Enjoy a final breakfast at your hotel. Cost: ~INR 300 (IDR 6,000).
- **Shopping:** Visit the Ubud Art Market or a local shop for souvenirs. Budget: ~INR 1,000 - 2,000 (IDR 20,000 - 40,000).
- **Transfer to Airport:** Hire a taxi or use a ride-hailing app to reach the airport. Cost: ~INR 1,200 - 1,500 (IDR 25,000 - 30,000).      

#### **Afternoon:**
- **Lunch:** Grab a quick meal at a local restaurant before your flight. Cost: ~INR 300 - 500 (IDR 6,000 - 10,000).

**Day 6 Cost Estimate:** ~INR 2,800 - 4,000 (IDR 56,000 - 80,000).

---

### **Total Cost Estimate for 6 Days**
- **Accommodation:** ~INR 12,000 - 18,000 (IDR 240,000 - 360,000) for 5 nights.
- **Transportation:** ~INR 8,000 - 12,000 (IDR 160,000 - 240,000) including airport transfers, scooters, and fast boats.
- **Food and Drinks:** ~INR 15,000 - 25,000 (IDR 300,000 - 500,000).
- **Attractions and Activities:** ~INR 8,000 - 12,000 (IDR 160,000 - 240,000).
- **Miscellaneous (Shopping, Souvenirs):** ~INR 3,000 - 5,000 (IDR 60,000 - 100,000).

**Total:** ~INR 46,000 - 72,000 (IDR 920,000 - 1,440,000).

---

### **Tips for Your Trip:**
1. **Local Transportation:** Renting a scooter is a cost-effective way to explore Bali. Cost: ~INR 300 - 500 per day (IDR 6,000 - 10,000).  
2. **Currency:** Exchange some Indian Rupees to Indonesian Rupiah (IDR) before your trip or at the airport.
3. **Weather:** June is part of Bali's dry season, so expect warm and sunny weather. Don’t forget to pack sunscreen and a hat.
4. **Respect Local Customs:** Bali is predominantly Hindu, so dress modestly when visiting temples.
5. **Insect Repellent:** Mosquitoes can be a nuisance, so carry insect repellent.

Enjoy your trip to Bali! 🌴

    **Hotels:**
    ```csv
HotelName,Description,Estimated Cost per night,currency code
The Farm Hostel,A chilled, friendly atmosphere with recent expansions,2000 INR,INR
Cozy Bobo Hostel,Cozy rooms in a friendly environment,2500 INR,INR
Canggu Beach Hostel,Big crowds, fun parties, poolside beers, 3-minutes from the beach,250 INR,INR
The ONE Legian Hotel,Modern amenities and rooftop pool in the heart of Kuta,3280 INR,INR
OYO 2854 COZY B&B SEMINYAK,Budget-friendly B&B with cozy rooms,2460 INR,INR
OYO 401 The Frog Homestay Sanur,Comfortable and affordable room options,2460 INR,INR
W Bali - Seminyak,Beachfront luxe and Bali-fused design with glamorous suites,12500 INR,INR
Four Seasons Resort Bali At Jimbaran Bay,Luxury resort with terraces and Asian fusion restaurant,12500 INR,INR
The St. Regis Bali Resort,Luxury hotel with fine dining and beachfront location,12500 INR,INR
```

    **Weather:**
    Error getting forecast: Bad API Request:Invalid location parameter value.**Bali Weather Summary for June 25th to 30th: Outdoor Trip Planning**

**Overview:**
Bali in late June is typically warm and dry, marking the end of the dry season. Expect mostly sunny days with occasional light rain showers, ideal for outdoor activities.

**Temperature:**
- Average: 26°C
- High: 29°C
- Low: 23°C

**Weather Conditions:**
- **Humidity:** Low, with average humidity levels.
- **Rainfall:** Minimal, with an average of 8-12 mm over six days.
- **Sunshine:** 9-10 hours per day, perfect for outdoor exploration.

**Best Places to Visit:**
- **Beaches:** Ideal for sunbathing and swimming.
- **Rice Terraces:** Accessible and scenic.
- **Volcanoes and Forests:** Great for hiking and trekking.

**Precautions:**
- **Sun Protection:** Sunscreen, hats, and sunglasses are essential.
- **Rain Gear:** Carry lightweight rain gear for unexpected showers.
- **Insect Repellent:** Protect against mosquitoes.
- **Hydration:** Stay hydrated due to heat and humidity.
- **Layering:** Bring light layers for cooler mountain evenings.

**Activity Tips:**
- **Timing:** Start early to avoid afternoon heat and potential showers.
- **Flexibility:** Plan for possible rain interruptions.
- **Sea Conditions:** Calm seas are good for water activities like snorkeling or diving.

**Additional Considerations:**
- **UV Index:** Be mindful of strong tropical sun.
- **Trail Conditions:** Check for any mud from unexpected rain.

Enjoy your trip with well-planned activities and necessary precautions for a memorable Bali experience.

    **Visa Info:**
    Consultant/company name,Details,number of working days for processing,Purpose,Estimated Cost,currency code
GoDigit,Visa on Arrival for Tourism,1,visa fee,2564,INR
GoDigit,Single Entry Tourist Visa,NA,visa fee,7692,INR
GoDigit,Multiple Entry Tourist Visa,NA,visa fee,15384,INR

AI Trip Planner Assistant End...
------------------------------------------------------------------------------------------

