"""
Crochet Pattern Project Planner - Complete Workflow
From pattern selection to purchase links and inspiration
"""

import streamlit as st
import pandas as pd
import chromadb
from datetime import datetime
import os
import requests

# Import your existing functions
import sys
sys.path.append('.')

from slice10_yarn_match import calculate_match_score, load_databases, normalize_yarn_weight

# Back to home navigation
st.markdown('<a href="/" class="back-home">← Back to Home</a>', unsafe_allow_html=True)

# City coordinates for weather API (300+ major world cities)
LOCATION_COORDS = {
    "Afghanistan (Kabul)": {"lat": 34.5553, "lon": 69.2075},
    "Albania (Tirana)": {"lat": 41.3275, "lon": 19.8187},
    "Algeria (Algiers)": {"lat": 36.7538, "lon": 3.0588},
    "Andorra (Andorra la Vella)": {"lat": 42.5063, "lon": 1.5218},
    "Angola (Luanda)": {"lat": -8.8383, "lon": 13.2344},
    "Argentina (Buenos Aires)": {"lat": -34.6037, "lon": -58.3816},
    "Argentina (Córdoba)": {"lat": -31.4201, "lon": -64.1888},
    "Argentina (Mendoza)": {"lat": -32.8895, "lon": -68.8458},
    "Argentina (Rosario)": {"lat": -32.9442, "lon": -60.6505},
    "Armenia (Yerevan)": {"lat": 40.1792, "lon": 44.4991},
    "Australia (Adelaide)": {"lat": -34.9285, "lon": 138.6007},
    "Australia (Brisbane)": {"lat": -27.4698, "lon": 153.0251},
    "Australia (Canberra)": {"lat": -35.2809, "lon": 149.1300},
    "Australia (Melbourne)": {"lat": -37.8136, "lon": 144.9631},
    "Australia (Perth)": {"lat": -31.9505, "lon": 115.8605},
    "Australia (Sydney)": {"lat": -33.8688, "lon": 151.2093},
    "Austria (Graz)": {"lat": 47.0707, "lon": 15.4395},
    "Austria (Innsbruck)": {"lat": 47.2692, "lon": 11.4041},
    "Austria (Salzburg)": {"lat": 47.8095, "lon": 13.0550},
    "Austria (Vienna)": {"lat": 48.2082, "lon": 16.3738},
    "Azerbaijan (Baku)": {"lat": 40.4093, "lon": 49.8671},
    "Bahamas (Nassau)": {"lat": 25.0343, "lon": -77.3963},
    "Bahrain (Manama)": {"lat": 26.2285, "lon": 50.5860},
    "Bangladesh (Chittagong)": {"lat": 22.3569, "lon": 91.7832},
    "Bangladesh (Dhaka)": {"lat": 23.8103, "lon": 90.4125},
    "Barbados (Bridgetown)": {"lat": 13.0969, "lon": -59.6145},
    "Belarus (Minsk)": {"lat": 53.9045, "lon": 27.5615},
    "Belgium (Antwerp)": {"lat": 51.2194, "lon": 4.4025},
    "Belgium (Brussels)": {"lat": 50.8503, "lon": 4.3517},
    "Belgium (Ghent)": {"lat": 51.0543, "lon": 3.7174},
    "Belize (Belmopan)": {"lat": 17.2510, "lon": -88.7590},
    "Benin (Porto-Novo)": {"lat": 6.4969, "lon": 2.6289},
    "Bhutan (Thimphu)": {"lat": 27.4728, "lon": 89.6390},
    "Bolivia (La Paz)": {"lat": -16.5000, "lon": -68.1500},
    "Bolivia (Santa Cruz)": {"lat": -17.7832, "lon": -63.1821},
    "Bosnia (Sarajevo)": {"lat": 43.8563, "lon": 18.4131},
    "Botswana (Gaborone)": {"lat": -24.6282, "lon": 25.9231},
    "Brazil (Belo Horizonte)": {"lat": -19.9167, "lon": -43.9345},
    "Brazil (Brasília)": {"lat": -15.7975, "lon": -47.8919},
    "Brazil (Curitiba)": {"lat": -25.4284, "lon": -49.2733},
    "Brazil (Fortaleza)": {"lat": -3.7172, "lon": -38.5433},
    "Brazil (Manaus)": {"lat": -3.1190, "lon": -60.0217},
    "Brazil (Porto Alegre)": {"lat": -30.0346, "lon": -51.2177},
    "Brazil (Recife)": {"lat": -8.0476, "lon": -34.8770},
    "Brazil (Rio de Janeiro)": {"lat": -22.9068, "lon": -43.1729},
    "Brazil (Salvador)": {"lat": -12.9714, "lon": -38.5014},
    "Brazil (São Paulo)": {"lat": -23.5505, "lon": -46.6333},
    "Brunei (Bandar Seri Begawan)": {"lat": 4.9031, "lon": 114.9398},
    "Bulgaria (Plovdiv)": {"lat": 42.1354, "lon": 24.7453},
    "Bulgaria (Sofia)": {"lat": 42.6977, "lon": 23.3219},
    "Bulgaria (Varna)": {"lat": 43.2141, "lon": 27.9147},
    "Burkina Faso (Ouagadougou)": {"lat": 12.3714, "lon": -1.5197},
    "Burundi (Gitega)": {"lat": -3.4271, "lon": 29.9246},
    "Cambodia (Phnom Penh)": {"lat": 11.5564, "lon": 104.9282},
    "Cameroon (Yaoundé)": {"lat": 3.8480, "lon": 11.5021},
    "Canada (Calgary)": {"lat": 51.0447, "lon": -114.0719},
    "Canada (Edmonton)": {"lat": 53.5461, "lon": -113.4938},
    "Canada (Halifax)": {"lat": 44.6488, "lon": -63.5752},
    "Canada (Montreal)": {"lat": 45.5017, "lon": -73.5673},
    "Canada (Ottawa)": {"lat": 45.4215, "lon": -75.6972},
    "Canada (Quebec City)": {"lat": 46.8139, "lon": -71.2080},
    "Canada (Toronto)": {"lat": 43.6532, "lon": -79.3832},
    "Canada (Vancouver)": {"lat": 49.2827, "lon": -123.1207},
    "Canada (Winnipeg)": {"lat": 49.8951, "lon": -97.1384},
    "Cape Verde (Praia)": {"lat": 14.9177, "lon": -23.5092},
    "Central African Rep (Bangui)": {"lat": 4.3947, "lon": 18.5582},
    "Chad (N'Djamena)": {"lat": 12.1348, "lon": 15.0557},
    "Chile (Santiago)": {"lat": -33.4489, "lon": -70.6693},
    "Chile (Valparaíso)": {"lat": -33.0472, "lon": -71.6127},
    "China (Beijing)": {"lat": 39.9042, "lon": 116.4074},
    "China (Chengdu)": {"lat": 30.5728, "lon": 104.0668},
    "China (Chongqing)": {"lat": 29.4316, "lon": 106.9123},
    "China (Guangzhou)": {"lat": 23.1291, "lon": 113.2644},
    "China (Hangzhou)": {"lat": 30.2741, "lon": 120.1551},
    "China (Hong Kong)": {"lat": 22.3193, "lon": 114.1694},
    "China (Nanjing)": {"lat": 32.0603, "lon": 118.7969},
    "China (Shanghai)": {"lat": 31.2304, "lon": 121.4737},
    "China (Shenzhen)": {"lat": 22.5431, "lon": 114.0579},
    "China (Tianjin)": {"lat": 39.3434, "lon": 117.3616},
    "China (Wuhan)": {"lat": 30.5928, "lon": 114.3055},
    "China (Xi'an)": {"lat": 34.2658, "lon": 108.9541},
    "Colombia (Barranquilla)": {"lat": 10.9685, "lon": -74.7813},
    "Colombia (Bogotá)": {"lat": 4.7110, "lon": -74.0721},
    "Colombia (Cali)": {"lat": 3.4516, "lon": -76.5320},
    "Colombia (Cartagena)": {"lat": 10.3910, "lon": -75.4794},
    "Colombia (Medellín)": {"lat": 6.2476, "lon": -75.5658},
    "Comoros (Moroni)": {"lat": -11.7172, "lon": 43.2473},
    "Congo (Brazzaville)": {"lat": -4.2634, "lon": 15.2429},
    "Congo (Kinshasa)": {"lat": -4.4419, "lon": 15.2663},
    "Costa Rica (San José)": {"lat": 9.9281, "lon": -84.0907},
    "Croatia (Dubrovnik)": {"lat": 42.6507, "lon": 18.0944},
    "Croatia (Split)": {"lat": 43.5081, "lon": 16.4402},
    "Croatia (Zagreb)": {"lat": 45.8150, "lon": 15.9819},
    "Cuba (Havana)": {"lat": 23.1136, "lon": -82.3666},
    "Cyprus (Nicosia)": {"lat": 35.1856, "lon": 33.3823},
    "Czech Republic (Brno)": {"lat": 49.1951, "lon": 16.6068},
    "Czech Republic (Prague)": {"lat": 50.0755, "lon": 14.4378},
    "Denmark (Aarhus)": {"lat": 56.1629, "lon": 10.2039},
    "Denmark (Copenhagen)": {"lat": 55.6761, "lon": 12.5683},
    "Djibouti (Djibouti)": {"lat": 11.8251, "lon": 42.5903},
    "Dominican Republic (Santo Domingo)": {"lat": 18.4861, "lon": -69.9312},
    "Ecuador (Guayaquil)": {"lat": -2.1894, "lon": -79.8890},
    "Ecuador (Quito)": {"lat": -0.1807, "lon": -78.4678},
    "Egypt (Alexandria)": {"lat": 31.2001, "lon": 29.9187},
    "Egypt (Cairo)": {"lat": 30.0444, "lon": 31.2357},
    "El Salvador (San Salvador)": {"lat": 13.6929, "lon": -89.2182},
    "Equatorial Guinea (Malabo)": {"lat": 3.7504, "lon": 8.7371},
    "Eritrea (Asmara)": {"lat": 15.3229, "lon": 38.9251},
    "Estonia (Tallinn)": {"lat": 59.4370, "lon": 24.7536},
    "Eswatini (Mbabane)": {"lat": -26.3054, "lon": 31.1367},
    "Ethiopia (Addis Ababa)": {"lat": 9.0320, "lon": 38.7469},
    "Fiji (Suva)": {"lat": -18.1248, "lon": 178.4501},
    "Finland (Espoo)": {"lat": 60.2055, "lon": 24.6559},
    "Finland (Helsinki)": {"lat": 60.1699, "lon": 24.9384},
    "Finland (Tampere)": {"lat": 61.4978, "lon": 23.7610},
    "Finland (Turku)": {"lat": 60.4518, "lon": 22.2666},
    "France (Bordeaux)": {"lat": 44.8378, "lon": -0.5792},
    "France (Lyon)": {"lat": 45.7640, "lon": 4.8357},
    "France (Marseille)": {"lat": 43.2965, "lon": 5.3698},
    "France (Nice)": {"lat": 43.7102, "lon": 7.2620},
    "France (Paris)": {"lat": 48.8566, "lon": 2.3522},
    "France (Strasbourg)": {"lat": 48.5734, "lon": 7.7521},
    "France (Toulouse)": {"lat": 43.6047, "lon": 1.4442},
    "Gabon (Libreville)": {"lat": 0.4162, "lon": 9.4673},
    "Gambia (Banjul)": {"lat": 13.4549, "lon": -16.5790},
    "Georgia (Tbilisi)": {"lat": 41.7151, "lon": 44.8271},
    "Germany (Berlin)": {"lat": 52.5200, "lon": 13.4050},
    "Germany (Bremen)": {"lat": 53.0793, "lon": 8.8017},
    "Germany (Cologne)": {"lat": 50.9375, "lon": 6.9603},
    "Germany (Dortmund)": {"lat": 51.5136, "lon": 7.4653},
    "Germany (Dresden)": {"lat": 51.0504, "lon": 13.7373},
    "Germany (Düsseldorf)": {"lat": 51.2277, "lon": 6.7735},
    "Germany (Essen)": {"lat": 51.4556, "lon": 7.0116},
    "Germany (Frankfurt)": {"lat": 50.1109, "lon": 8.6821},
    "Germany (Hamburg)": {"lat": 53.5511, "lon": 9.9937},
    "Germany (Hanover)": {"lat": 52.3759, "lon": 9.7320},
    "Germany (Leipzig)": {"lat": 51.3397, "lon": 12.3731},
    "Germany (Munich)": {"lat": 48.1351, "lon": 11.5820},
    "Germany (Nuremberg)": {"lat": 49.4521, "lon": 11.0767},
    "Germany (Stuttgart)": {"lat": 48.7758, "lon": 9.1829},
    "Ghana (Accra)": {"lat": 5.6037, "lon": -0.1870},
    "Greece (Athens)": {"lat": 37.9838, "lon": 23.7275},
    "Greece (Thessaloniki)": {"lat": 40.6401, "lon": 22.9444},
    "Greenland (Nuuk)": {"lat": 64.1814, "lon": -51.6941},
    "Guatemala (Guatemala City)": {"lat": 14.6349, "lon": -90.5069},
    "Guinea (Conakry)": {"lat": 9.6412, "lon": -13.5784},
    "Guyana (Georgetown)": {"lat": 6.8013, "lon": -58.1551},
    "Haiti (Port-au-Prince)": {"lat": 18.5944, "lon": -72.3074},
    "Honduras (Tegucigalpa)": {"lat": 14.0723, "lon": -87.1921},
    "Hungary (Budapest)": {"lat": 47.4979, "lon": 19.0402},
    "Hungary (Debrecen)": {"lat": 47.5316, "lon": 21.6273},
    "Iceland (Reykjavik)": {"lat": 64.1466, "lon": -21.9426},
    "India (Ahmedabad)": {"lat": 23.0225, "lon": 72.5714},
    "India (Bangalore)": {"lat": 12.9716, "lon": 77.5946},
    "India (Chennai)": {"lat": 13.0827, "lon": 80.2707},
    "India (Delhi)": {"lat": 28.7041, "lon": 77.1025},
    "India (Hyderabad)": {"lat": 17.3850, "lon": 78.4867},
    "India (Jaipur)": {"lat": 26.9124, "lon": 75.7873},
    "India (Kolkata)": {"lat": 22.5726, "lon": 88.3639},
    "India (Mumbai)": {"lat": 19.0760, "lon": 72.8777},
    "India (Pune)": {"lat": 18.5204, "lon": 73.8567},
    "India (Surat)": {"lat": 21.1702, "lon": 72.8311},
    "Indonesia (Bandung)": {"lat": -6.9175, "lon": 107.6191},
    "Indonesia (Jakarta)": {"lat": -6.2088, "lon": 106.8456},
    "Indonesia (Medan)": {"lat": 3.5952, "lon": 98.6722},
    "Indonesia (Surabaya)": {"lat": -7.2575, "lon": 112.7521},
    "Iran (Isfahan)": {"lat": 32.6546, "lon": 51.6680},
    "Iran (Mashhad)": {"lat": 36.2605, "lon": 59.6168},
    "Iran (Shiraz)": {"lat": 29.5918, "lon": 52.5836},
    "Iran (Tabriz)": {"lat": 38.0962, "lon": 46.2738},
    "Iran (Tehran)": {"lat": 35.6892, "lon": 51.3890},
    "Iraq (Baghdad)": {"lat": 33.3152, "lon": 44.3661},
    "Iraq (Basra)": {"lat": 30.5085, "lon": 47.7835},
    "Ireland (Cork)": {"lat": 51.8985, "lon": -8.4756},
    "Ireland (Dublin)": {"lat": 53.3498, "lon": -6.2603},
    "Ireland (Galway)": {"lat": 53.2707, "lon": -9.0568},
    "Israel (Haifa)": {"lat": 32.7940, "lon": 34.9896},
    "Israel (Jerusalem)": {"lat": 31.7683, "lon": 35.2137},
    "Israel (Tel Aviv)": {"lat": 32.0853, "lon": 34.7818},
    "Italy (Bologna)": {"lat": 44.4949, "lon": 11.3426},
    "Italy (Florence)": {"lat": 43.7696, "lon": 11.2558},
    "Italy (Genoa)": {"lat": 44.4056, "lon": 8.9463},
    "Italy (Milan)": {"lat": 45.4642, "lon": 9.1900},
    "Italy (Naples)": {"lat": 40.8518, "lon": 14.2681},
    "Italy (Palermo)": {"lat": 38.1157, "lon": 13.3615},
    "Italy (Rome)": {"lat": 41.9028, "lon": 12.4964},
    "Italy (Turin)": {"lat": 45.0703, "lon": 7.6869},
    "Italy (Venice)": {"lat": 45.4408, "lon": 12.3155},
    "Ivory Coast (Abidjan)": {"lat": 5.3600, "lon": -4.0083},
    "Jamaica (Kingston)": {"lat": 17.9714, "lon": -76.7931},
    "Japan (Fukuoka)": {"lat": 33.5904, "lon": 130.4017},
    "Japan (Hiroshima)": {"lat": 34.3853, "lon": 132.4553},
    "Japan (Kobe)": {"lat": 34.6901, "lon": 135.1955},
    "Japan (Kyoto)": {"lat": 35.0116, "lon": 135.7681},
    "Japan (Nagoya)": {"lat": 35.1815, "lon": 136.9066},
    "Japan (Osaka)": {"lat": 34.6937, "lon": 135.5023},
    "Japan (Sapporo)": {"lat": 43.0642, "lon": 141.3469},
    "Japan (Tokyo)": {"lat": 35.6762, "lon": 139.6503},
    "Japan (Yokohama)": {"lat": 35.4437, "lon": 139.6380},
    "Jordan (Amman)": {"lat": 31.9454, "lon": 35.9284},
    "Kazakhstan (Almaty)": {"lat": 43.2220, "lon": 76.8512},
    "Kazakhstan (Nur-Sultan)": {"lat": 51.1694, "lon": 71.4491},
    "Kenya (Mombasa)": {"lat": -4.0435, "lon": 39.6682},
    "Kenya (Nairobi)": {"lat": -1.2864, "lon": 36.8172},
    "Kuwait (Kuwait City)": {"lat": 29.3759, "lon": 47.9774},
    "Kyrgyzstan (Bishkek)": {"lat": 42.8746, "lon": 74.5698},
    "Laos (Vientiane)": {"lat": 17.9757, "lon": 102.6331},
    "Latvia (Riga)": {"lat": 56.9496, "lon": 24.1052},
    "Lebanon (Beirut)": {"lat": 33.8886, "lon": 35.4955},
    "Lesotho (Maseru)": {"lat": -29.3167, "lon": 27.4833},
    "Liberia (Monrovia)": {"lat": 6.2907, "lon": -10.7605},
    "Libya (Tripoli)": {"lat": 32.8872, "lon": 13.1913},
    "Liechtenstein (Vaduz)": {"lat": 47.1410, "lon": 9.5209},
    "Lithuania (Vilnius)": {"lat": 54.6872, "lon": 25.2797},
    "Luxembourg (Luxembourg)": {"lat": 49.6116, "lon": 6.1319},
    "Madagascar (Antananarivo)": {"lat": -18.8792, "lon": 47.5079},
    "Malawi (Lilongwe)": {"lat": -13.9626, "lon": 33.7741},
    "Malaysia (Johor Bahru)": {"lat": 1.4927, "lon": 103.7414},
    "Malaysia (Kuala Lumpur)": {"lat": 3.1390, "lon": 101.6869},
    "Malaysia (Penang)": {"lat": 5.4141, "lon": 100.3288},
    "Maldives (Malé)": {"lat": 4.1755, "lon": 73.5093},
    "Mali (Bamako)": {"lat": 12.6392, "lon": -8.0029},
    "Malta (Valletta)": {"lat": 35.8989, "lon": 14.5146},
    "Mauritania (Nouakchott)": {"lat": 18.0735, "lon": -15.9582},
    "Mauritius (Port Louis)": {"lat": -20.1609, "lon": 57.5012},
    "Mexico (Guadalajara)": {"lat": 20.6597, "lon": -103.3496},
    "Mexico (Mexico City)": {"lat": 19.4326, "lon": -99.1332},
    "Mexico (Monterrey)": {"lat": 25.6866, "lon": -100.3161},
    "Mexico (Puebla)": {"lat": 19.0414, "lon": -98.2063},
    "Mexico (Tijuana)": {"lat": 32.5149, "lon": -117.0382},
    "Moldova (Chișinău)": {"lat": 47.0105, "lon": 28.8638},
    "Monaco (Monaco)": {"lat": 43.7384, "lon": 7.4246},
    "Mongolia (Ulaanbaatar)": {"lat": 47.8864, "lon": 106.9057},
    "Montenegro (Podgorica)": {"lat": 42.4304, "lon": 19.2594},
    "Morocco (Casablanca)": {"lat": 33.5731, "lon": -7.5898},
    "Morocco (Marrakech)": {"lat": 31.6295, "lon": -7.9811},
    "Morocco (Rabat)": {"lat": 34.0209, "lon": -6.8416},
    "Mozambique (Maputo)": {"lat": -25.9655, "lon": 32.5832},
    "Myanmar (Mandalay)": {"lat": 21.9588, "lon": 96.0891},
    "Myanmar (Yangon)": {"lat": 16.8661, "lon": 96.1951},
    "Namibia (Windhoek)": {"lat": -22.5597, "lon": 17.0832},
    "Nepal (Kathmandu)": {"lat": 27.7172, "lon": 85.3240},
    "Netherlands (Amsterdam)": {"lat": 52.3676, "lon": 4.9041},
    "Netherlands (Rotterdam)": {"lat": 51.9225, "lon": 4.4792},
    "Netherlands (The Hague)": {"lat": 52.0705, "lon": 4.3007},
    "Netherlands (Utrecht)": {"lat": 52.0907, "lon": 5.1214},
    "New Zealand (Auckland)": {"lat": -36.8485, "lon": 174.7633},
    "New Zealand (Christchurch)": {"lat": -43.5321, "lon": 172.6362},
    "New Zealand (Wellington)": {"lat": -41.2865, "lon": 174.7762},
    "Nicaragua (Managua)": {"lat": 12.1150, "lon": -86.2362},
    "Niger (Niamey)": {"lat": 13.5127, "lon": 2.1128},
    "Nigeria (Abuja)": {"lat": 9.0765, "lon": 7.3986},
    "Nigeria (Ibadan)": {"lat": 7.3775, "lon": 3.9470},
    "Nigeria (Kano)": {"lat": 12.0022, "lon": 8.5920},
    "Nigeria (Lagos)": {"lat": 6.5244, "lon": 3.3792},
    "North Korea (Pyongyang)": {"lat": 39.0392, "lon": 125.7625},
    "North Macedonia (Skopje)": {"lat": 41.9973, "lon": 21.4280},
    "Norway (Bergen)": {"lat": 60.3913, "lon": 5.3221},
    "Norway (Oslo)": {"lat": 59.9139, "lon": 10.7522},
    "Norway (Stavanger)": {"lat": 58.9700, "lon": 5.7331},
    "Norway (Trondheim)": {"lat": 63.4305, "lon": 10.3951},
    "Oman (Muscat)": {"lat": 23.5880, "lon": 58.3829},
    "Pakistan (Faisalabad)": {"lat": 31.4180, "lon": 73.0790},
    "Pakistan (Islamabad)": {"lat": 33.6844, "lon": 73.0479},
    "Pakistan (Karachi)": {"lat": 24.8607, "lon": 67.0011},
    "Pakistan (Lahore)": {"lat": 31.5204, "lon": 74.3587},
    "Pakistan (Rawalpindi)": {"lat": 33.5651, "lon": 73.0169},
    "Panama (Panama City)": {"lat": 8.9824, "lon": -79.5199},
    "Papua New Guinea (Port Moresby)": {"lat": -9.4438, "lon": 147.1803},
    "Paraguay (Asunción)": {"lat": -25.2637, "lon": -57.5759},
    "Peru (Arequipa)": {"lat": -16.4090, "lon": -71.5375},
    "Peru (Lima)": {"lat": -12.0464, "lon": -77.0428},
    "Philippines (Cebu City)": {"lat": 10.3157, "lon": 123.8854},
    "Philippines (Davao)": {"lat": 7.1907, "lon": 125.4553},
    "Philippines (Manila)": {"lat": 14.5995, "lon": 120.9842},
    "Philippines (Quezon City)": {"lat": 14.6760, "lon": 121.0437},
    "Poland (Gdansk)": {"lat": 54.3520, "lon": 18.6466},
    "Poland (Krakow)": {"lat": 50.0647, "lon": 19.9450},
    "Poland (Lodz)": {"lat": 51.7592, "lon": 19.4560},
    "Poland (Poznan)": {"lat": 52.4064, "lon": 16.9252},
    "Poland (Warsaw)": {"lat": 52.2297, "lon": 21.0122},
    "Poland (Wroclaw)": {"lat": 51.1079, "lon": 17.0385},
    "Portugal (Lisbon)": {"lat": 38.7223, "lon": -9.1393},
    "Portugal (Porto)": {"lat": 41.1579, "lon": -8.6291},
    "Qatar (Doha)": {"lat": 25.2854, "lon": 51.5310},
    "Romania (Bucharest)": {"lat": 44.4268, "lon": 26.1025},
    "Romania (Cluj-Napoca)": {"lat": 46.7712, "lon": 23.6236},
    "Romania (Timișoara)": {"lat": 45.7489, "lon": 21.2087},
    "Russia (Kazan)": {"lat": 55.8304, "lon": 49.0661},
    "Russia (Moscow)": {"lat": 55.7558, "lon": 37.6173},
    "Russia (Nizhny Novgorod)": {"lat": 56.2965, "lon": 43.9361},
    "Russia (Novosibirsk)": {"lat": 55.0084, "lon": 82.9357},
    "Russia (Saint Petersburg)": {"lat": 59.9311, "lon": 30.3609},
    "Russia (Vladivostok)": {"lat": 43.1332, "lon": 131.9113},
    "Russia (Yekaterinburg)": {"lat": 56.8389, "lon": 60.6057},
    "Rwanda (Kigali)": {"lat": -1.9403, "lon": 30.0619},
    "Saudi Arabia (Jeddah)": {"lat": 21.2854, "lon": 39.2376},
    "Saudi Arabia (Mecca)": {"lat": 21.3891, "lon": 39.8579},
    "Saudi Arabia (Medina)": {"lat": 24.5247, "lon": 39.5692},
    "Saudi Arabia (Riyadh)": {"lat": 24.7136, "lon": 46.6753},
    "Senegal (Dakar)": {"lat": 14.7167, "lon": -17.4677},
    "Serbia (Belgrade)": {"lat": 44.7866, "lon": 20.4489},
    "Serbia (Novi Sad)": {"lat": 45.2671, "lon": 19.8335},
    "Seychelles (Victoria)": {"lat": -4.6796, "lon": 55.4920},
    "Sierra Leone (Freetown)": {"lat": 8.4657, "lon": -13.2317},
    "Singapore (Singapore)": {"lat": 1.3521, "lon": 103.8198},
    "Slovakia (Bratislava)": {"lat": 48.1486, "lon": 17.1077},
    "Slovenia (Ljubljana)": {"lat": 46.0569, "lon": 14.5058},
    "Somalia (Mogadishu)": {"lat": 2.0469, "lon": 45.3182},
    "South Africa (Cape Town)": {"lat": -33.9249, "lon": 18.4241},
    "South Africa (Durban)": {"lat": -29.8587, "lon": 31.0218},
    "South Africa (Johannesburg)": {"lat": -26.2041, "lon": 28.0473},
    "South Africa (Pretoria)": {"lat": -25.7479, "lon": 28.2293},
    "South Korea (Busan)": {"lat": 35.1796, "lon": 129.0756},
    "South Korea (Incheon)": {"lat": 37.4563, "lon": 126.7052},
    "South Korea (Seoul)": {"lat": 37.5665, "lon": 126.9780},
    "South Sudan (Juba)": {"lat": 4.8594, "lon": 31.5713},
    "Spain (Barcelona)": {"lat": 41.3874, "lon": 2.1686},
    "Spain (Bilbao)": {"lat": 43.2630, "lon": -2.9350},
    "Spain (Madrid)": {"lat": 40.4168, "lon": -3.7038},
    "Spain (Málaga)": {"lat": 36.7213, "lon": -4.4214},
    "Spain (Seville)": {"lat": 37.3891, "lon": -5.9845},
    "Spain (Valencia)": {"lat": 39.4699, "lon": -0.3763},
    "Spain (Zaragoza)": {"lat": 41.6488, "lon": -0.8891},
    "Sri Lanka (Colombo)": {"lat": 6.9271, "lon": 79.8612},
    "Sudan (Khartoum)": {"lat": 15.5007, "lon": 32.5599},
    "Suriname (Paramaribo)": {"lat": 5.8520, "lon": -55.2038},
    "Sweden (Gothenburg)": {"lat": 57.7089, "lon": 11.9746},
    "Sweden (Malmö)": {"lat": 55.6050, "lon": 13.0038},
    "Sweden (Stockholm)": {"lat": 59.3293, "lon": 18.0686},
    "Sweden (Uppsala)": {"lat": 59.8586, "lon": 17.6389},
    "Switzerland (Basel)": {"lat": 47.5596, "lon": 7.5886},
    "Switzerland (Bern)": {"lat": 46.9480, "lon": 7.4474},
    "Switzerland (Geneva)": {"lat": 46.2044, "lon": 6.1432},
    "Switzerland (Lausanne)": {"lat": 46.5197, "lon": 6.6323},
    "Switzerland (Zurich)": {"lat": 47.3769, "lon": 8.5417},
    "Syria (Aleppo)": {"lat": 36.2021, "lon": 37.1343},
    "Syria (Damascus)": {"lat": 33.5138, "lon": 36.2765},
    "Taiwan (Kaohsiung)": {"lat": 22.6273, "lon": 120.3014},
    "Taiwan (Taichung)": {"lat": 24.1477, "lon": 120.6736},
    "Taiwan (Taipei)": {"lat": 25.0330, "lon": 121.5654},
    "Tajikistan (Dushanbe)": {"lat": 38.5598, "lon": 68.7738},
    "Tanzania (Dar es Salaam)": {"lat": -6.7924, "lon": 39.2083},
    "Tanzania (Dodoma)": {"lat": -6.1630, "lon": 35.7516},
    "Thailand (Bangkok)": {"lat": 13.7563, "lon": 100.5018},
    "Thailand (Chiang Mai)": {"lat": 18.7883, "lon": 98.9853},
    "Thailand (Phuket)": {"lat": 7.8804, "lon": 98.3923},
    "Togo (Lomé)": {"lat": 6.1256, "lon": 1.2254},
    "Trinidad and Tobago (Port of Spain)": {"lat": 10.6596, "lon": -61.5089},
    "Tunisia (Tunis)": {"lat": 36.8065, "lon": 10.1815},
    "Turkey (Ankara)": {"lat": 39.9334, "lon": 32.8597},
    "Turkey (Antalya)": {"lat": 36.8969, "lon": 30.7133},
    "Turkey (Bursa)": {"lat": 40.1826, "lon": 29.0665},
    "Turkey (Istanbul)": {"lat": 41.0082, "lon": 28.9784},
    "Turkey (Izmir)": {"lat": 38.4237, "lon": 27.1428},
    "Turkmenistan (Ashgabat)": {"lat": 37.9601, "lon": 58.3261},
    "Uganda (Kampala)": {"lat": 0.3476, "lon": 32.5825},
    "Ukraine (Dnipro)": {"lat": 48.4647, "lon": 35.0462},
    "Ukraine (Kharkiv)": {"lat": 49.9935, "lon": 36.2304},
    "Ukraine (Kyiv)": {"lat": 50.4501, "lon": 30.5234},
    "Ukraine (Lviv)": {"lat": 49.8397, "lon": 24.0297},
    "Ukraine (Odesa)": {"lat": 46.4825, "lon": 30.7233},
    "United Arab Emirates (Abu Dhabi)": {"lat": 24.4539, "lon": 54.3773},
    "United Arab Emirates (Dubai)": {"lat": 25.2048, "lon": 55.2708},
    "United Arab Emirates (Sharjah)": {"lat": 25.3463, "lon": 55.4209},
    "UK (Belfast)": {"lat": 54.5973, "lon": -5.9301},
    "UK (Birmingham)": {"lat": 52.4862, "lon": -1.8904},
    "UK (Bristol)": {"lat": 51.4545, "lon": -2.5879},
    "UK (Cardiff)": {"lat": 51.4816, "lon": -3.1791},
    "UK (Edinburgh)": {"lat": 55.9533, "lon": -3.1883},
    "UK (Glasgow)": {"lat": 55.8642, "lon": -4.2518},
    "UK (Leeds)": {"lat": 53.8008, "lon": -1.5491},
    "UK (Liverpool)": {"lat": 53.4084, "lon": -2.9916},
    "UK (London)": {"lat": 51.5074, "lon": -0.1278},
    "UK (Manchester)": {"lat": 53.4808, "lon": -2.2426},
    "UK (Newcastle)": {"lat": 54.9783, "lon": -1.6178},
    "UK (Nottingham)": {"lat": 52.9548, "lon": -1.1581},
    "UK (Sheffield)": {"lat": 53.3811, "lon": -1.4701},
    "Uruguay (Montevideo)": {"lat": -34.9011, "lon": -56.1645},
    "USA (Albuquerque)": {"lat": 35.0844, "lon": -106.6504},
    "USA (Atlanta)": {"lat": 33.7490, "lon": -84.3880},
    "USA (Austin)": {"lat": 30.2672, "lon": -97.7431},
    "USA (Baltimore)": {"lat": 39.2904, "lon": -76.6122},
    "USA (Boston)": {"lat": 42.3601, "lon": -71.0589},
    "USA (Charlotte)": {"lat": 35.2271, "lon": -80.8431},
    "USA (Chicago)": {"lat": 41.8781, "lon": -87.6298},
    "USA (Columbus)": {"lat": 39.9612, "lon": -82.9988},
    "USA (Dallas)": {"lat": 32.7767, "lon": -96.7970},
    "USA (Denver)": {"lat": 39.7392, "lon": -104.9903},
    "USA (Detroit)": {"lat": 42.3314, "lon": -83.0458},
    "USA (El Paso)": {"lat": 31.7619, "lon": -106.4850},
    "USA (Fort Worth)": {"lat": 32.7555, "lon": -97.3308},
    "USA (Honolulu)": {"lat": 21.3099, "lon": -157.8581},
    "USA (Houston)": {"lat": 29.7604, "lon": -95.3698},
    "USA (Indianapolis)": {"lat": 39.7684, "lon": -86.1581},
    "USA (Jacksonville)": {"lat": 30.3322, "lon": -81.6557},
    "USA (Kansas City)": {"lat": 39.0997, "lon": -94.5786},
    "USA (Las Vegas)": {"lat": 36.1699, "lon": -115.1398},
    "USA (Los Angeles)": {"lat": 34.0522, "lon": -118.2437},
    "USA (Memphis)": {"lat": 35.1495, "lon": -90.0490},
    "USA (Miami)": {"lat": 25.7617, "lon": -80.1918},
    "USA (Milwaukee)": {"lat": 43.0389, "lon": -87.9065},
    "USA (Minneapolis)": {"lat": 44.9778, "lon": -93.2650},
    "USA (Nashville)": {"lat": 36.1627, "lon": -86.7816},
    "USA (New Orleans)": {"lat": 29.9511, "lon": -90.0715},
    "USA (New York)": {"lat": 40.7128, "lon": -74.0060},
    "USA (Oklahoma City)": {"lat": 35.4676, "lon": -97.5164},
    "USA (Philadelphia)": {"lat": 39.9526, "lon": -75.1652},
    "USA (Phoenix)": {"lat": 33.4484, "lon": -112.0740},
    "USA (Portland)": {"lat": 45.5152, "lon": -122.6784},
    "USA (Raleigh)": {"lat": 35.7796, "lon": -78.6382},
    "USA (Sacramento)": {"lat": 38.5816, "lon": -121.4944},
    "USA (San Antonio)": {"lat": 29.4241, "lon": -98.4936},
    "USA (San Diego)": {"lat": 32.7157, "lon": -117.1611},
    "USA (San Francisco)": {"lat": 37.7749, "lon": -122.4194},
    "USA (San Jose)": {"lat": 37.3382, "lon": -121.8863},
    "USA (Seattle)": {"lat": 47.6062, "lon": -122.3321},
    "USA (Washington DC)": {"lat": 38.9072, "lon": -77.0369},
    "Uzbekistan (Tashkent)": {"lat": 41.2995, "lon": 69.2401},
    "Venezuela (Caracas)": {"lat": 10.4806, "lon": -66.9036},
    "Venezuela (Maracaibo)": {"lat": 10.6666, "lon": -71.6123},
    "Venezuela (Valencia)": {"lat": 10.1621, "lon": -68.0078},
    "Vietnam (Da Nang)": {"lat": 16.0544, "lon": 108.2022},
    "Vietnam (Hanoi)": {"lat": 21.0285, "lon": 105.8542},
    "Vietnam (Ho Chi Minh City)": {"lat": 10.8231, "lon": 106.6297},
    "Yemen (Sana'a)": {"lat": 15.5527, "lon": 48.5164},
    "Zambia (Lusaka)": {"lat": -15.3875, "lon": 28.3228},
    "Zimbabwe (Harare)": {"lat": -17.8252, "lon": 31.0335},
}

# Temperature-based location data (fallback if API fails)
LOCATION_TEMPS = {
    "Sweden (Stockholm)": {"winter": -3, "spring": 5, "summer": 18, "fall": 8},
    "Spain (Madrid)": {"winter": 6, "spring": 14, "summer": 25, "fall": 15},
    "UK (London)": {"winter": 5, "spring": 11, "summer": 18, "fall": 12},
    "USA (New York)": {"winter": 0, "spring": 12, "summer": 24, "fall": 13},
    "Canada (Toronto)": {"winter": -4, "spring": 9, "summer": 22, "fall": 10},
    "Australia (Sydney)": {"winter": 13, "spring": 18, "summer": 23, "fall": 19},
    "Germany (Berlin)": {"winter": 0, "spring": 9, "summer": 19, "fall": 10},
    "France (Paris)": {"winter": 4, "spring": 11, "summer": 20, "fall": 12},
    "Italy (Rome)": {"winter": 8, "spring": 14, "summer": 25, "fall": 17},
    "Netherlands (Amsterdam)": {"winter": 3, "spring": 10, "summer": 17, "fall": 11},
    "Custom": {"winter": 10, "spring": 15, "summer": 20, "fall": 12}
}

# Page config
st.set_page_config(
    page_title="Crochet Project Planner",
    page_icon="🧶",
    layout="wide"
)

# Initialize
@st.cache_data
def load_data():
    patterns_df, yarn_df = load_databases()
    return patterns_df, yarn_df

@st.cache_resource
def load_vector_db():
    try:
        client = chromadb.PersistentClient(path="./chroma_db")
        collection = client.get_collection(name="crochet_patterns")
        return client, collection
    except:
        # Vector DB not available in deployment - return None
        return None, None

def get_current_season():
    """Determine current season based on month"""
    month = datetime.now().month
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    else:
        return "fall"

@st.cache_data(ttl=1800)  # Cache for 30 minutes
def get_real_time_weather(location):
    """Fetch real-time temperature from OpenWeatherMap API"""
    if location == "Custom" or location not in LOCATION_COORDS:
        return None
    
    try:
        coords = LOCATION_COORDS[location]
        # Using OpenWeatherMap free API (no key needed for basic current weather)
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&current_weather=true&temperature_unit=celsius"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            temp = data.get('current_weather', {}).get('temperature')
            if temp is not None:
                return round(temp)
    except Exception as e:
        # If API fails, return None to use fallback
        return None
    
    return None

def get_temp_for_location_and_season(location, season):
    """Get average temperature for location and season"""
    return LOCATION_TEMPS.get(location, LOCATION_TEMPS["Custom"])[season]

def get_yarn_temp_range(yarn_row):
    """Determine comfortable temperature range for yarn based on composition and thickness"""
    cotton = yarn_row.get('Cotton (%)', 0)
    linen = yarn_row.get('Linen (%)', 0)
    bamboo = yarn_row.get('Bamboo/Viscouse (%)', 0)
    acrylic = yarn_row.get('Acrylic (%)', 0)
    wool = yarn_row.get('Wool (%)', 0)
    mohair = yarn_row.get('Mohair/Alpaca (%)', 0)
    
    # Get yarn thickness for warmth adjustment
    thickness = str(yarn_row.get('Yarn thikness', '')).lower()
    thickness_multiplier = 1.0
    
    # Thicker yarn = warmer at same composition
    if 'super bulky' in thickness or 'jumbo' in thickness:
        thickness_multiplier = 1.4
    elif 'bulky' in thickness or 'chunky' in thickness:
        thickness_multiplier = 1.25
    elif 'worsted' in thickness or 'aran' in thickness:
        thickness_multiplier = 1.1
    elif 'dk' in thickness or 'light worsted' in thickness:
        thickness_multiplier = 1.0
    elif 'sport' in thickness or 'baby' in thickness:
        thickness_multiplier = 0.9
    elif 'fingering' in thickness or 'sock' in thickness:
        thickness_multiplier = 0.8
    elif 'lace' in thickness or 'thread' in thickness:
        thickness_multiplier = 0.7
    
    # Calculate warmth based on fiber composition
    cool_fiber_pct = cotton + linen + bamboo  # Breathable, cool
    warm_fiber_pct = wool + mohair  # Insulating, warm
    
    # Base temperature ranges
    if warm_fiber_pct > 50:
        base_min, base_max, base_ideal = -10, 15, 5
        fiber_type = "Warm (Wool/Alpaca)"
    elif cool_fiber_pct > 50:
        base_min, base_max, base_ideal = 15, 35, 22
        fiber_type = "Cool (Cotton/Linen)"
    elif acrylic > 70:
        base_min, base_max, base_ideal = 5, 20, 12
        fiber_type = "All-season (Acrylic)"
    else:
        base_min, base_max, base_ideal = 5, 25, 15
        fiber_type = "Blend"
    
    # Adjust for thickness (thicker = shifts toward cooler temps)
    # For warm fibers: thicker extends cold tolerance
    # For cool fibers: thicker reduces heat tolerance
    if warm_fiber_pct > 50:
        adjusted_min = base_min - (5 * (thickness_multiplier - 1))
        adjusted_max = base_max + (3 * (thickness_multiplier - 1))
    elif cool_fiber_pct > 50:
        adjusted_min = base_min + (5 * (thickness_multiplier - 1))
        adjusted_max = base_max - (3 * (thickness_multiplier - 1))
    else:
        adjusted_min = base_min
        adjusted_max = base_max
    
    return {
        "min": int(adjusted_min),
        "max": int(adjusted_max),
        "ideal": base_ideal,
        "type": f"{fiber_type} ({thickness.title() if thickness else 'Standard'})"
    }

def calculate_temp_match_score(yarn_temp_range, current_temp):
    """Calculate how well yarn matches current temperature (0-30 points)"""
    yarn_min = yarn_temp_range["min"]
    yarn_max = yarn_temp_range["max"]
    yarn_ideal = yarn_temp_range["ideal"]
    
    if yarn_min <= current_temp <= yarn_max:
        # Inside range - calculate distance from ideal
        distance_from_ideal = abs(current_temp - yarn_ideal)
        score = 30 - (distance_from_ideal * 1.5)
        return max(0, score)
    else:
        # Outside range - steep penalty
        if current_temp < yarn_min:
            distance = yarn_min - current_temp
        else:
            distance = current_temp - yarn_max
        score = 30 - (distance * 3)
        return max(0, score)

def determine_yarn_season(yarn_row):
    """Determine if yarn is suitable for current season based on composition"""
    # Summer yarns: cotton, linen, bamboo
    summer_score = yarn_row.get('Cotton (%)', 0) + yarn_row.get('Linen (%)', 0) + yarn_row.get('Bamboo/Viscouse (%)', 0)
    
    # Winter yarns: wool, mohair, alpaca
    winter_score = yarn_row.get('Wool (%)', 0) + yarn_row.get('Mohair/Alpaca (%)', 0)
    
    # All-season: acrylic, blends
    allseason_score = yarn_row.get('Acrylic (%)', 0)
    
    if summer_score > 50:
        return "Summer"
    elif winter_score > 50:
        return "Winter"
    elif allseason_score > 70:
        return "All-Season"
    else:
        return "Spring/Fall"

def get_yarn_store_url(yarn_name, brand):
    """Generate potential store URLs for yarn"""
    # This is a simplified version - you'd need actual URL mapping
    yarn_clean = yarn_name.lower().replace(' ', '-')
    brand_clean = str(brand).lower() if pd.notna(brand) else 'hobbii'
    
    urls = []
    
    # Hobbii
    urls.append(f"https://hobbii.com/search?q={yarn_clean}")
    
    # Katia
    if 'katia' in brand_clean:
        urls.append(f"https://www.katia.com/ES/yarns.html?q={yarn_clean}")
    
    return urls

# Load data
patterns_df, yarn_df = load_data()
client, collection = load_vector_db()

# Get unique patterns (remove duplicates)
unique_patterns = patterns_df.drop_duplicates(subset=['Pattern Name'])
current_season = get_current_season()

# Header
st.title("🧶 Crochet Project Planner")

# Location selector at top
col_header1, col_header2 = st.columns([2, 1])

with col_header1:
    user_location = st.selectbox(
        "📍 Your Location",
        list(LOCATION_TEMPS.keys()),
        index=0,
        help="Select your location for temperature-based yarn recommendations"
    )

with col_header2:
    if user_location == "Custom":
        # Custom location - allow manual temperature input
        current_temp = st.number_input(
            "🌡️ Current Temp (°C)",
            min_value=-20,
            max_value=40,
            value=15,
            step=1,
            help="Enter your current temperature"
        )
    else:
        # Try to get real-time weather for selected location
        real_temp = get_real_time_weather(user_location)
        
        if real_temp is not None:
            # Use real-time temperature
            current_temp = real_temp
            st.success(f"🌡️ Live: {real_temp}°C")
        else:
            # Fallback to seasonal average
            current_temp = get_temp_for_location_and_season(user_location, current_season)
            st.info(f"🌡️ {current_temp}°C ({current_season})")

st.markdown(f"🌡️ **Temperature-based recommendations for {user_location}** | Current: **{current_temp}°C**")
st.markdown("---")

# Sidebar - Browse patterns
st.sidebar.header("🔍 Find Your Pattern")

# Search
search_query = st.sidebar.text_input("Search patterns", placeholder="e.g., baby blanket, summer top")

# Filters
st.sidebar.subheader("Filters")

# Favorites filter
if 'favorites' in st.session_state and st.session_state.favorites:
    show_favorites_only = st.sidebar.checkbox(f"⭐ Show favorites only ({len(st.session_state.favorites)})")
else:
    show_favorites_only = False

difficulties = ["All"] + sorted(unique_patterns['Difficulty Level'].dropna().unique().tolist())
selected_difficulty = st.sidebar.selectbox("Difficulty", difficulties)

yarn_weights = ["All"] + sorted(unique_patterns['Yarn Weight'].dropna().unique().tolist())
selected_yarn_weight = st.sidebar.selectbox("Yarn Weight", yarn_weights)

# Advanced Filters
with st.sidebar.expander("🔧 Advanced Filters"):
    # Season filter
    season_filter = st.multiselect(
        "Best Season",
        ["Spring", "Summer", "Fall", "Winter"],
        help="Filter by recommended season"
    )
    
    # Project type filter
    project_type = st.selectbox(
        "Project Type",
        ["All", "Clothing", "Home Decor", "Toys/Amigurumi", "Accessories"],
        help="Filter by type of project"
    )
    
    # Estimated time filter
    time_estimate = st.selectbox(
        "Time to Complete",
        ["All", "Quick (< 5 hours)", "Weekend (5-20 hours)", "Week (20-40 hours)", "Long-term (40+ hours)"],
        help="Estimated time to complete"
    )
    
    # Color complexity
    color_count = st.selectbox(
        "Color Complexity",
        ["All", "1 Color", "2-3 Colors", "4+ Colors"],
        help="Number of colors needed"
    )

# Apply filters
filtered_df = unique_patterns.copy()

# Favorites filter
if show_favorites_only and 'favorites' in st.session_state:
    filtered_df = filtered_df[filtered_df['Pattern Name'].isin(st.session_state.favorites)]

if selected_difficulty != "All":
    filtered_df = filtered_df[filtered_df['Difficulty Level'] == selected_difficulty]

if selected_yarn_weight != "All":
    filtered_df = filtered_df[filtered_df['Yarn Weight'] == selected_yarn_weight]

# Advanced Filters Application
if season_filter:
    # Infer season from yarn composition and weight
    # Cool yarns (cotton) = Summer/Spring, Warm yarns (wool) = Winter/Fall
    season_mask = filtered_df['Recommended Yarn Composition'].str.contains('cotton|linen', case=False, na=False)
    if "Summer" in season_filter or "Spring" in season_filter:
        filtered_df = filtered_df[season_mask]
    elif "Winter" in season_filter or "Fall" in season_filter:
        filtered_df = filtered_df[~season_mask]

if project_type != "All":
    # Infer project type from pattern name/structure
    type_patterns = {
        "Clothing": r'top|shirt|sweater|cardigan|dress|pants|skirt|hat|scarf',
        "Home Decor": r'blanket|cushion|pillow|basket|rug|coaster',
        "Toys/Amigurumi": r'ami|toy|doll|animal|plush|bear|bunny',
        "Accessories": r'bag|pouch|purse|keychain|headband|mitt'
    }
    if project_type in type_patterns:
        pattern = type_patterns[project_type]
        mask = filtered_df['Pattern Name'].str.contains(pattern, case=False, na=False) | \
               filtered_df['Pattern Structure'].str.contains(pattern, case=False, na=False)
        filtered_df = filtered_df[mask]

if time_estimate != "All":
    # Estimate based on difficulty and structure
    if time_estimate == "Quick (< 5 hours)":
        filtered_df = filtered_df[filtered_df['Difficulty Level'].isin(['Beginner', 'Easy'])]
    elif time_estimate == "Weekend (5-20 hours)":
        filtered_df = filtered_df[filtered_df['Difficulty Level'].isin(['Easy', 'Intermediate'])]
    elif time_estimate == "Week (20-40 hours)":
        filtered_df = filtered_df[filtered_df['Difficulty Level'] == 'Intermediate']
    elif time_estimate == "Long-term (40+ hours)":
        filtered_df = filtered_df[filtered_df['Difficulty Level'].isin(['Advanced', 'Expert'])]

if color_count != "All":
    # Infer from recommended colors if available
    if "Recommended Colors" in filtered_df.columns:
        if color_count == "1 Color":
            mask = filtered_df['Recommended Colors'].str.contains(r'^\d+$', na=False) & \
                   (filtered_df['Recommended Colors'].astype(str).str.extract(r'(\d+)', expand=False).astype(float) == 1)
            filtered_df = filtered_df[mask | filtered_df['Recommended Colors'].isna()]

if search_query:
    # Simple text search
    mask = filtered_df['Pattern Name'].str.contains(search_query, case=False, na=False) | \
           filtered_df['Pattern Structure'].str.contains(search_query, case=False, na=False) | \
           filtered_df['Stitches Required'].str.contains(search_query, case=False, na=False)
    filtered_df = filtered_df[mask]

# Main area - Pattern selection
st.sidebar.markdown("---")
st.sidebar.markdown(f"**{len(filtered_df)} patterns found**")

selected_pattern_name = st.sidebar.selectbox(
    "Select a pattern",
    filtered_df['Pattern Name'].tolist()
)

# Get selected pattern details
selected_pattern = filtered_df[filtered_df['Pattern Name'] == selected_pattern_name].iloc[0]

# MAIN CONTENT - PROJECT PLANNING

# Section 1: Pattern Overview
col_header_pattern, col_fav = st.columns([4, 1])

with col_header_pattern:
    st.header(f"📋 {selected_pattern['Pattern Name']}")

with col_fav:
    # Simple favorite toggle (stores in session state)
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    
    is_favorite = selected_pattern['Pattern Name'] in st.session_state.favorites
    
    if st.button("⭐ Favorite" if not is_favorite else "💫 Favorited", key="fav_btn"):
        if is_favorite:
            st.session_state.favorites.remove(selected_pattern['Pattern Name'])
        else:
            st.session_state.favorites.append(selected_pattern['Pattern Name'])
        st.rerun()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Difficulty", selected_pattern['Difficulty Level'])
with col2:
    st.metric("Yarn Weight", selected_pattern['Yarn Weight'])
with col3:
    st.metric("Hook Size", f"{selected_pattern['Hook Size (mm)']}mm")
with col4:
    st.metric("Structure", selected_pattern['Pattern Structure'][:20] + "...")

st.markdown("---")

# Section 2: Stitches Needed
st.subheader("🪡 Stitches You'll Need")
stitches = str(selected_pattern['Stitches Required']).split(',')
st.markdown("**Required stitches:**")

# Display stitches as pills
stitch_html = ""
for stitch in stitches:
    stitch = stitch.strip()
    stitch_html += f'<span style="background-color: #E8F4F8; padding: 5px 10px; border-radius: 15px; margin: 5px; display: inline-block;">{stitch}</span>'

st.markdown(stitch_html, unsafe_allow_html=True)

st.markdown("""
💡 **New to these stitches?** Search YouTube for tutorials:
- [Single Crochet (sc)](https://www.youtube.com/results?search_query=crochet+single+crochet+tutorial)
- [Double Crochet (dc)](https://www.youtube.com/results?search_query=crochet+double+crochet+tutorial)
""")

st.markdown("---")

# Section 3: Yarn Recommendations (TEMPERATURE-AWARE)
st.subheader(f"🧵 Top Yarn Recommendations for {current_temp}°C")

# Calculate match scores for all yarns
yarn_matches = []
for idx, yarn_row in yarn_df.iterrows():
    # Base pattern match score
    base_score = calculate_match_score(selected_pattern, yarn_row)
    
    # Temperature suitability score
    yarn_temp_range = get_yarn_temp_range(yarn_row)
    temp_score = calculate_temp_match_score(yarn_temp_range, current_temp)
    
    # Combined: 70% pattern match + 30% temperature match
    total_score = (base_score * 0.7) + temp_score
    
    yarn_matches.append({
        'name': yarn_row['Name of the product'],
        'score': total_score,
        'base_score': base_score,
        'temp_score': temp_score,
        'price': yarn_row['Price (€)'],
        'rating': yarn_row['Rating (★)'],
        'brand': yarn_row.get('Brand', 'Unknown'),
        'temp_range': yarn_temp_range,
        'cotton': yarn_row.get('Cotton (%)', 0),
        'acrylic': yarn_row.get('Acrylic (%)', 0),
        'wool': yarn_row.get('Wool (%)', 0),
        'weight': yarn_row.get('Yarn thikness', 'Unknown')
    })

# Sort and get top 3
yarn_matches_df = pd.DataFrame(yarn_matches).sort_values('score', ascending=False).head(3)

for idx, yarn in yarn_matches_df.iterrows():
    with st.expander(f"✨ {yarn['name']} - {yarn['score']:.0f}% Match", expanded=(idx==0)):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**Price:** €{yarn['price']:.2f} per ball")
            st.markdown(f"**Rating:** {'⭐' * int(yarn['rating'])}")
            
            # Temperature comfort info
            temp_range = yarn['temp_range']
            st.markdown(f"**Fiber Type:** {temp_range['type']}")
            st.markdown(f"**Comfort Range:** {temp_range['min']}°C to {temp_range['max']}°C (ideal: {temp_range['ideal']}°C)")
            
            # Temperature match indicator
            if temp_range['min'] <= current_temp <= temp_range['max']:
                distance = abs(current_temp - temp_range['ideal'])
                if distance <= 3:
                    st.success(f"🌡️ Perfect for {current_temp}°C!")
                elif distance <= 7:
                    st.info(f"✅ Good for {current_temp}°C")
                else:
                    st.warning(f"⚠️ Usable at {current_temp}°C but not ideal")
            else:
                if current_temp < temp_range['min']:
                    st.error(f"❄️ Too cold for this yarn ({current_temp}°C < {temp_range['min']}°C)")
                else:
                    st.error(f"🔥 Too hot for this yarn ({current_temp}°C > {temp_range['max']}°C)")
            
            st.markdown(f"**Weight:** {yarn['weight']}")
            
            # Composition
            comp_parts = []
            if yarn['cotton'] > 0:
                comp_parts.append(f"{int(yarn['cotton'])}% Cotton")
            if yarn['acrylic'] > 0:
                comp_parts.append(f"{int(yarn['acrylic'])}% Acrylic")
            if yarn['wool'] > 0:
                comp_parts.append(f"{int(yarn['wool'])}% Wool")
            
            st.markdown(f"**Composition:** {', '.join(comp_parts)}")
            
            # Score breakdown
            with st.expander("📊 Score Breakdown"):
                st.markdown(f"- Pattern Match: {yarn['base_score']:.1f}%")
                st.markdown(f"- Temperature Match: {yarn['temp_score']:.1f}/30 pts")
                st.markdown(f"- **Total: {yarn['score']:.1f}%**")
        
        with col2:
            st.markdown("**Where to Buy:**")
            urls = get_yarn_store_url(yarn['name'], yarn['brand'])
            for url in urls:
                if 'hobbii' in url:
                    st.markdown(f"🛒 [Hobbii.com]({url})")
                elif 'katia' in url:
                    st.markdown(f"🛒 [Katia.es]({url})")

st.markdown("---")

# Section 4: Color Inspiration
st.subheader("🎨 Color Inspiration")

color_info = str(selected_pattern.get('Recommended Colors', 'Not specified'))
st.markdown(f"**Pattern suggests:** {color_info}")

st.markdown("""
💡 **Need color ideas?** Check out these resources:
- [Coolors.co](https://coolors.co/generate) - Color palette generator
- [Pinterest Color Palettes](https://www.pinterest.com/search/pins/?q=crochet%20color%20palette)
- [Ravelry Color Inspiration](https://www.ravelry.com/)
""")

# Pinterest search link for this specific pattern
pinterest_search = selected_pattern['Pattern Name'].replace(' ', '%20')
st.markdown(f"🔍 [Search '{selected_pattern['Pattern Name']}' on Pinterest](https://www.pinterest.com/search/pins/?q={pinterest_search}%20crochet)")

st.markdown("---")

# Section 5: Materials Checklist
st.subheader("📦 Complete Materials List")

materials = str(selected_pattern['Materials Needed'])
st.markdown(materials)

st.markdown("---")

# Section 6: Project Cost Calculator
st.subheader("💰 Project Cost Estimator")

col_calc1, col_calc2 = st.columns(2)

with col_calc1:
    num_balls = st.number_input("Estimated balls/skeins needed", min_value=1, max_value=50, value=3, help="Check pattern for yarn requirements")
    
    if yarn_matches_df.iloc[0] is not None:
        selected_yarn_for_calc = yarn_matches_df.iloc[0]
        yarn_cost = selected_yarn_for_calc['price'] * num_balls
        
        st.markdown(f"**Yarn cost:** €{yarn_cost:.2f}")
        st.markdown(f"**Hook:** €5-15 (if needed)")
        st.markdown(f"**Notions:** €2-5")
        
        total_min = yarn_cost + 0
        total_max = yarn_cost + 20
        
        st.success(f"**Total Project Cost: €{total_min:.2f} - €{total_max:.2f}**")

with col_calc2:
    st.markdown("**Shopping List:**")
    shopping_list = f"""
    ✅ {selected_pattern['Pattern Name']}
    
    Materials:
    - {num_balls} balls of {yarn_matches_df.iloc[0]['name']}
    - {selected_pattern['Hook Size (mm)']}mm crochet hook
    - Scissors
    - Yarn needle
    - {selected_pattern['Materials Needed'][:100]}...
    
    Estimated Budget: €{total_min:.2f} - €{total_max:.2f}
    """
    
    st.download_button(
        label="📋 Download Shopping List",
        data=shopping_list,
        file_name=f"{selected_pattern['Pattern Name']}_shopping_list.txt",
        mime="text/plain"
    )

st.markdown("---")

# Section 7: Pattern PDF
st.subheader("📄 Pattern PDF")

pdf_filename = selected_pattern['Source File']
pdf_path = os.path.join('PDFPatterns', pdf_filename)

if os.path.exists(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()
    
    st.download_button(
        label="📥 Download Pattern PDF",
        data=pdf_bytes,
        file_name=pdf_filename,
        mime="application/pdf"
    )
    
    st.info(f"💾 Pattern saved as: {pdf_filename}")
else:
    st.warning(f"PDF not found: {pdf_filename}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Built with ❤️ for crochet enthusiasts | Season-aware yarn recommendations | Direct purchase links</p>
</div>
""", unsafe_allow_html=True)
