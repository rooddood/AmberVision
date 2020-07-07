var vm = new Vue({
  el: '#app',
  data: {
    map: null,
    tileLayer: null,
    pic: null,
    updated_pic: null,
    results: null,
    all_results: null,
    imageSelected: false,
    test_list: ['../test_92/92_20200119_142929_detected.png','../test_92/92_20200120_142401_detected.png'],
    prediction_list: ['../test_102/102_20200119_142932_detected.png','../test_102/102_20200119_142424_detected.png'],
    fake_cam_data: {
      camId: '92',
      name: 'K St @ 17th St & Conneticut Ave',
      type: 'marker',
      coords: [38.902599, -77.039233],
      orientation: "WEST"
    },
    query_name: 'Test name',
    layers: [
      {
        id: 0,
        name: 'Cameras',
        active: true,
        //to add all cameras
        features: [
                  {
                    id: 0,
                    camId: '1',
                    name: 'K St @ 17th St & Conneticut Ave',
                    type: 'marker',
                    coords: [38.902599, -77.039233],
                    orientation: "WEST"
                  },
                  {
                    id: 1,
                    camId: '2',
                    name: 'New Hampshire Ave @ Georgia Ave',
                    type: 'marker',
                    coords: [38.936701, -77.024232],
                    orientation: "SOUTH"
                  },
                  {
                    id: 2,
                    camId: '3',
                    name: 'M St @ Francis Scott Key Brdg',
                    type: 'marker',
                    coords: [38.905143, -77.068561],
                    orientation: "WEST",
                  },
                  {
                    id: 3,
                    camId: '4',
                    name: 'M St @ S Capitol St',
                    type: 'marker',
                    coords: [38.876366, -77.009061],
                    orientation: "EAST"
                  },
                  {
                    id: 4,
                    camId: '5',
                    name: 'Florida Ave @ New York Ave',
                    type: 'marker',
                    coords: [38.909042, -77.004583],
                    orientation: "WEST"
                  },
                  {
                    id: 5,
                    camId: '6',
                    name: 'Eastern Ave @ Kenilworth Ave',
                    type: 'marker',
                    coords: [38.91218, -76.934167],
                    orientation: "EAST",
                  },
                  {
                    id: 6,
                    camId: '7',
                    name: '4th St @ New York Ave',
                    type: 'marker',
                    coords: [38.904965, -77.016301],
                    orientation: "SOUTH"
                  },
                  {
                    id: 7,
                    camId: '8',
                    name: '14th St Brdg',
                    type: 'marker',
                    coords: [38.882427, -77.032657],
                    orientation: "NORTH"
                  },
                  {
                    id: 8,
                    camId: '9',
                    name: 'Ist St @ Delaware Ave',
                    type: 'marker',
                    coords: [38.879356, -77.013071],
                    orientation: "WEST",
                  },
                  {
                    id: 9,
                    camId: '10',
                    name: 'Georgia Ave @ Irving St',
                    type: 'marker',
                    coords: [38.928978, -77.023337],
                    orientation: "SOUTH"
                  },
                  {
                    id: 10,
                    camId: '11',
                    name: '16th St @ U St',
                    type: 'marker',
                    coords: [38.917113, -77.036378],
                    orientation: "NORTH",
                  },
                  {
                    id: 11,
                    camId: '12',
                    name: '16th St @ Columbia Rd',
                    type: 'marker',
                    coords: [38.926386, -77.036587],
                    orientation: "SOUTH",
                  },
                  {
                    id: 12,
                    camId: '13',
                    name: 'Georgia Ave @ Eastern Ave',
                    type: 'marker',
                    coords: [38.984507, -77.02673],
                    orientation: "SOUTH"
                  },
                  {
                    id: 13,
                    camId: '14',
                    name: '16th St @ Irving St',
                    type: 'marker',
                    coords: [38.928585, -77.036372],
                    orientation: "NORTH"
                  },
                  {
                    id: 14,
                    camId: '15',
                    name: 'Georgia Ave @ Kansas Ave',
                    type: 'marker',
                    coords: [38.942045, -77.025678],
                    orientation: "SOUTH",
                  },
                  {
                    id: 15,
                    camId: '16',
                    name: 'S Capitol St @ Suitland Pkwy',
                    type: 'marker',
                    coords: [38.865266, -77.001454],
                    orientation: "NORTH"
                  },
                  {
                    id: 16,
                    camId: '17',
                    name: 'Pennsylvania Ave @ SE Fwy',
                    type: 'marker',
                    coords: [38.877887, -76.980316],
                    orientation: "SOUTH"
                  },
                  {
                    id: 17,
                    camId: '18',
                    name: 'New York Ave @ Bladensburg Rd',
                    type: 'marker',
                    coords: [38.917474, -76.972542],
                    orientation: "WEST",
                  },
                  {
                    id: 18,
                    camId: '19',
                    name: 'Independence Ave @ 7th St',
                    type: 'marker',
                    coords: [38.887455, -77.022099],
                    orientation: "EAST"
                  },
                  {
                    id: 19,
                    camId: '20',
                    name: 'Connecticut Ave @ Calvert St',
                    type: 'marker',
                    coords: [38.92368, -77.051737],
                    orientation: "SOUTH"
                  },
                  {
                    id: 20,
                    camId: '21',
                    name: 'Maryland Ave @ H St & Benning Rd',
                    type: 'marker',
                    coords: [38.900211, -76.982939],
                    orientation: "EAST",
                  },
                  {
                    id: 21,
                    camId: '22',
                    name: 'Rhode Island Ave @ S Dakota Ave',
                    type: 'marker',
                    coords: [38.931351, -76.971433],
                    orientation: "WEST",
                  },
                  {
                    id: 22,
                    camId: '23',
                    name: 'E Capitol St @ Benning Rd',
                    type: 'marker',
                    coords: [38.889599,  -76.937291],
                    orientation: "EAST",
                  },
                  {
                    id: 23,
                    camId: '24',
                    name: 'Benning Rd @ Minnesota Ave',
                    type: 'marker',
                    coords: [38.895112,-76.94945],
                    orientation: "EAST",
                  },
                  {
                    id: 24,
                    camId: '25',
                    name: 'Pennsylvania Ave @ 7th St',
                    type: 'marker',
                    coords: [38.893522, -77.022118],
                    orientation: "WEST",
                  },
                  {
                    id: 25,
                    camId: '26',
                    name: 'E Capitol St @ Southern Ave',
                    type: 'marker',
                    coords: [38.889616, -76.913367],
                    orientation: "EAST",
                  },
                  {
                    id: 26,
                    camId: '27',
                    name: 'Dupont Circle @ Connecticut Ave',
                    type: 'marker',
                    coords: [38.910295,  -77.043674],
                    orientation: "WEST",
                  },
                  {
                    id: 27,
                    camId: '28',
                    name: 'Whitehurst Fwy @ 27th St & K St',
                    type: 'marker',
                    coords: [38.90236, -77.056277],
                    orientation: "EAST",
                  },
                  {
                    id: 28,
                    camId: '29',
                    name: 'Wisconsin Ave @ Massachusetts Ave',
                    type: 'marker',
                    coords: [38.928829, -77.073308],
                    orientation: "SOUTH",
                  },
                  {
                    id: 29,
                    camId: '30',
                    name: 'Canal Rd @ Foxhall Rd',
                    type: 'marker',
                    coords: [38.905852,  -77.079084],
                    orientation: "EAST",
                  },
                  {
                    id: 30,
                    camId: '31',
                    name: 'Connecticut Ave @ Macomb St',
                    type: 'marker',
                    coords: [38.933615, -77.057259],
                    orientation: "NORTH",
                  },
                  {
                    id: 31,
                    camId: '32',
                    name: 'Connecticut Ave @ Florida Ave',
                    type: 'marker',
                    coords: [38.914016, -77.04618],
                    orientation: "SOUTH",
                  },
                  {
                    id: 29,
                    camId: '30',
                    name: 'Canal Rd @ Foxhall Rd',
                    type: 'marker',
                    coords: [38.905852,  -77.079084],
                    orientation: "EAST",
                  },
                  {
                    id: 30,
                    camId: '31',
                    name: 'Connecticut Ave @ Macomb St',
                    type: 'marker',
                    coords: [38.933615, -77.057259],
                    orientation: "NORTH",
                  },
                  {
                    id: 31,
                    camId: '32',
                    name: 'Connecticut Ave @ Florida Ave',
                    type: 'marker',
                    coords: [38.914016, -77.04618],
                    orientation: "SOUTH",
                  },
                  {
                    id: 32,
                    camId: '33',
                    name: 'MacArthur Blvd @ Loughboro Rd',
                    type: 'marker',
                    coords: [38.93582,  -77.111663],
                    orientation: "NORTH",
                  },
                  {
                    id: 33,
                    camId: '34',
                    name: '16th St @ Colorado Ave',
                    type: 'marker',
                    coords: [38.952255, -77.036513],
                    orientation: "SOUTH",
                  },
                  {
                    id: 34,
                    camId: '35',
                    name: 'Pennsylvania Ave @ 2nd St & Independence Ave',
                    type: 'marker',
                    coords: [38.887721, -77.003454],
                    orientation: "WEST",
                  },
                  {
                    id: 35,
                    camId: '36',
                    name: 'Pennsylvania Ave @ 8th St',
                    type: 'marker',
                    coords: [38.8841, -76.994872],
                    orientation: "SOUTH",
                  },
                  {
                    id: 36,
                    camId: '37',
                    name: 'K St @ 19th St',
                    type: 'marker',
                    coords: [38.902605,  -77.043605],
                    orientation: "WEST",
                  },
                  {
                    id: 37,
                    camId: '38',
                    name: '24th St @ Washington Circle',
                    type: 'marker',
                    coords: [38.902598, -77.051338],
                    orientation: "NORTH",
                  },
                  {
                    id: 38,
                    camId: '39',
                    name: 'H St @ 3rd St',
                    type: 'marker',
                    coords: [38.9001, -77.002188],
                    orientation: "WEST",
                  },
                  {
                    id: 39,
                    camId: '40',
                    name: '7th St @ H St',
                    type: 'marker',
                    coords: [38.899688,  -77.022019],
                    orientation: "SOUTH",
                  },
                  {
                    id: 40,
                    camId: '41',
                    name: 'Benning Rd @ 36th St',
                    type: 'marker',
                    coords: [38.895862, -76.954186],
                    orientation: "EAST",
                  },
                  {
                    id: 41,
                    camId: '42',
                    name: 'E Capitol St @ 58th St',
                    type: 'marker',
                    coords: [38.889744, -76.917658],
                    orientation: "WEST",
                  },
                  {
                    id: 42,
                    camId: '43',
                    name: 'New York Ave @ 9th St',
                    type: 'marker',
                    coords: [38.913675,  -76.990527],
                    orientation: "EAST",
                  },
                  {
                    id: 43,
                    camId: '44',
                    name: 'New York Ave @ N Capitol St',
                    type: 'marker',
                    coords: [38.907463, -77.008997],
                    orientation: "WEST",
                  },
                  {
                    id: 44,
                    camId: '45',
                    name: '7th St @ New York Ave & Mt Vernon Pl',
                    type: 'marker',
                    coords: [38.902815, -77.022025],
                    orientation: "SOUTH",
                  },
                  {
                    id: 45,
                    camId: '46',
                    name: '7th St @ Rhode Island Ave',
                    type: 'marker',
                    coords: [38.912449,  -77.022024],
                    orientation: "SOUTH",
                  },
                  {
                    id: 46,
                    camId: '47',
                    name: 'Rhode Island Ave @ Florida Ave',
                    type: 'marker',
                    coords: [38.914141, -77.017133],
                    orientation: "WEST",
                  },
                  {
                    id: 47,
                    camId: '48',
                    name: 'Rhode Island Ave @ 18th St',
                    type: 'marker',
                    coords: [38.927619, -76.979231],
                    orientation: "WEST",
                  },
                  {
                    id: 48,
                    camId: '49',
                    name: 'Constitution Ave @ 3rd St',
                    type: 'marker',
                    coords: [38.891961,  -77.014981],
                    orientation: "EAST",
                  },
                  {
                    id: 49,
                    camId: '50',
                    name: '14th St @ Pennsylvania Ave',
                    type: 'marker',
                    coords: [38.896254, -77.031819],
                    orientation: "NORTH",
                  },
                  {
                    id: 50,
                    camId: '51',
                    name: 'Virginia Ave @ E St',
                    type: 'marker',
                    coords: [38.89608,  -77.048395],
                    orientation: "SOUTH",
                  },
                  {
                    id: 51,
                    camId: '52',
                    name: 'Scott Circle @ 16th St',
                    type: 'marker',
                    coords: [38.907545,  -77.036435],
                    orientation: "SOUTH",
                  },
                  {
                    id: 52,
                    camId: '53',
                    name: 'Georgia Ave @ Missouri Ave',
                    type: 'marker',
                    coords: [38.961122, -77.028139],
                    orientation: "SOUTH",
                  },
                  {
                    id: 53,
                    camId: '54',
                    name: 'Upshur St @ 16th St',
                    type: 'marker',
                    coords: [38.941954, -77.036338],
                    orientation: "NORTH",
                  },
                  {
                    id: 54,
                    camId: '55',
                    name: '16th St @ Missouri Ave & Military Rd',
                    type: 'marker',
                    coords: [38.962442,  -77.036282],
                    orientation: "NORTH",
                  },
                  {
                    id: 55,
                    camId: '56',
                    name: '12th St @ Constitution Ave',
                    type: 'marker',
                    coords: [38.892306, -77.028276],
                    orientation: "SOUTH",
                  },
                  {
                    id: 56,
                    camId: '57',
                    name: '9th St @ Constitution Ave',
                    type: 'marker',
                    coords: [38.892269,  -77.024097],
                    orientation: "SOUTH",
                  },
                  {
                    id: 57,
                    camId: '58',
                    name: 'Independence Ave @ Washington Ave',
                    type: 'marker',
                    coords: [38.887654,  -77.014117],
                    orientation: "WEST",
                  },
                  {
                    id: 58,
                    camId: '59',
                    name: 'M St @ Wisconsin Ave',
                    type: 'marker',
                    coords: [38.905089, -77.062642],
                    orientation: "EAST",
                  },
                  {
                    id: 59,
                    camId: '60',
                    name: 'S Capitol St @ Southern Ave',
                    type: 'marker',
                    coords: [38.821233, -77.001479],
                    orientation: "SOUTH",
                  },
                  {
                  	id: 60,
                  	camId: '61',
                  	name: 'Branch Ave @ Pennsylvania Ave',
                  	type: 'marker',
                  	coords: [38.869422, -76.960313],
                  	orientation: "NORTH",
                  },
                  {
                  	id: 61,
                  	camId: '62',
                  	name: 'Western Ave @ Wisconsin Ave',
                  	type: 'marker',
                  	coords: [38.960769, -77.085913],
                  	orientation: "WEST",
                  },
                  {
                  	id: 62,
                  	camId: '63',
                  	name: 'Connecticut Ave @ Oliver St',
                  	type: 'marker',
                  	coords: [38.966871, -77.07672],
                  	orientation: "EAST",
                  },
                  {
                  	id: 63,
                  	camId: '64',
                  	name: 'Connecticut Ave @ Nebraska Ave',
                  	type: 'marker',
                  	coords: [38.955823, -77.070423],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 64,
                  	camId: '65',
                  	name: 'Wisconsin Ave @ Nebraska Ave & Tenley Crl',
                  	type: 'marker',
                  	coords: [38.946523, -77.079038],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 65,
                  	camId: '66',
                  	name: 'Wisconsin Ave @ Calvert St',
                  	type: 'marker',
                  	coords: [38.922461, -77.073002],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 66,
                  	camId: '67',
                  	name: 'Connecticut Ave @ Van Ness St',
                  	type: 'marker',
                  	coords: [38.943035, -77.062978],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 67,
                  	camId: '68',
                  	name: 'MacArthur Blvd @ Arizona Ave',
                  	type: 'marker',
                  	coords: [38.927211, -77.104071],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 68,
                  	camId: '69',
                  	name: '16th St @ K St',
                  	type: 'marker',
                  	coords: [38.902448, -77.036355],
                  	orientation: "NORTH",
                  },
                  {
                  	id: 69,
                  	camId: '70',
                  	name: 'Constitution Ave @ 15th St',
                  	type: 'marker',
                  	coords: [38.892212, -77.033831],
                  	orientation: "WEST",
                  },
                  {
                  	id: 70,
                  	camId: '71',
                  	name: 'Pennsylvania Ave @ Minnesota Ave',
                  	type: 'marker',
                  	coords: [38.873333, -76.970765],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 71,
                  	camId: '72',
                  	name: 'Pennsylvania Ave @ Alabama Ave',
                  	type: 'marker',
                  	coords: [38.865477, -76.951258],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 72,
                  	camId: '73',
                  	name: 'Pennsylvania Ave @ 9th St',
                  	type: 'marker',
                  	coords: [38.893686, -77.024092],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 73,
                  	camId: '74',
                  	name: 'Pennsylvania Ave @ M St & 28th St',
                  	type: 'marker',
                  	coords: [38.905165, -77.057453],
                  	orientation: "NORTH",
                  },
                  {
                  	id: 74,
                  	camId: '75',
                  	name: 'Alabama Ave @ Branch Ave',
                  	type: 'marker',
                  	coords: [38.862, -76.958894],
                  	orientation: "WEST",
                  },
                  {
                  	id: 75,
                  	camId: '76',
                  	name: 'Branch Ave @ Southern Ave',
                  	type: 'marker',
                  	coords: [38.854907, -76.958208],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 76,
                  	camId: '77',
                  	name: 'K St @ 21st St',
                  	type: 'marker',
                  	coords: [38.902447, -77.046506],
                  	orientation: "EAST",
                  },
                  {
                  	id: 77,
                  	camId: '78',
                  	name: 'H St @ Massachusetts Ave & 3rd St',
                  	type: 'marker',
                  	coords: [38.89989, -77.014865],
                  	orientation: "EAST",
                  },
                  {
                  	id: 78,
                  	camId: '79',
                  	name: 'H St @ 2nd St',
                  	type: 'marker',
                  	coords: [38.900309, -77.013755],
                  	orientation: "WEST",
                  },
                  {
                  	id: 79,
                  	camId: '80',
                  	name: 'New York Ave @ New Jersey Ave',
                  	type: 'marker',
                  	coords: [38.905163, -77.015014],
                  	orientation: "EAST",
                  },
                  {
                  	id: 80,
                  	camId: '81',
                  	name: 'Constitution Ave @ 17th St',
                  	type: 'marker',
                  	coords: [38.892221, -77.039654],
                  	orientation: "WEST",
                  },
                  {
                  	id: 81,
                  	camId: '82',
                  	name: 'Constitution Ave @ 23rd St',
                  	type: 'marker',
                  	coords: [38.891985, -77.049949],
                  	orientation: "EAST",
                  },
                  {
                  	id: 82,
                  	camId: '83',
                  	name: 'Georgia Ave @ Arkansas Ave',
                  	type: 'marker',
                  	coords: [38.951619, -77.027279],
                  	orientation: "NORTH",
                  },
                  {
                  	id: 83,
                  	camId: '84',
                  	name: 'Wisconsin Ave @ Q St',
                  	type: 'marker',
                  	coords: [38.910701, -77.065184],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 84,
                  	camId: '85',
                  	name: 'Connecticut Ave @ Cathedral Ave',
                  	type: 'marker',
                  	coords: [38.928246, -77.054386],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 85,
                  	camId: '86',
                  	name: 'S Capitol St @ Atlantic St & Mississippi Ave',
                  	type: 'marker',
                  	coords: [38.831494, -77.007588],
                  	orientation: "NORTH",
                  },
                  {
                  	id: 86,
                  	camId: '87',
                  	name: '7th St @ Frontage St',
                  	type: 'marker',
                  	coords: [38.88278, -77.022148],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 87,
                  	camId: '88',
                  	name: 'N Capitol St @ H St',
                  	type: 'marker',
                  	coords: [38.900343, -77.009251],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 88,
                  	camId: '89',
                  	name: 'Constitution Ave @ 20th St',
                  	type: 'marker',
                  	coords: [38.891975, -77.045043],
                  	orientation: "EAST",
                  },
                  {
                  	id: 89,
                  	camId: '90',
                  	name: '14th St @ Independence Ave',
                  	type: 'marker',
                  	coords: [38.887402, -77.031956],
                  	orientation: "NORTH",
                  },
                  {
                  	id: 90,
                  	camId: '91',
                  	name: 'H St @ 14th St',
                  	type: 'marker',
                  	coords: [38.900149, -77.03176],
                  	orientation: "EAST",
                  },
                  {
                  	id: 91,
                  	camId: '92',
                  	name: '14th St @ New York Ave',
                  	type: 'marker',
                  	coords: [38.899637, -77.031821],
                  	orientation: "NORTH",
                  },
                  {
                  	id: 92,
                  	camId: '93',
                  	name: '16th St @ Alaska Ave',
                  	type: 'marker',
                  	coords: [38.975112, -77.036258],
                  	orientation: "NORTH",
                  },
                  {
                  	id: 93,
                  	camId: '94',
                  	name: '17th St @ E St',
                  	type: 'marker',
                  	coords: [38.895493, -77.039598],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 94,
                  	camId: '95',
                  	name: 'Pennsylvania Ave @ 17th St',
                  	type: 'marker',
                  	coords: [38.898742, -77.039612],
                  	orientation: "EAST",
                  },
                  {
                  	id: 95,
                  	camId: '96',
                  	name: '19th St @ Pennsylvania Ave',
                  	type: 'marker',
                  	coords: [38.900371, -77.043592],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 96,
                  	camId: '97',
                  	name: 'Pennsylvania Ave @ 21st St',
                  	type: 'marker',
                  	coords: [38.901154, -77.046554],
                  	orientation: "EAST",
                  },
                  {
                  	id: 97,
                  	camId: '98',
                  	name: 'H St @ Connecticut Ave & Jackson Pl',
                  	type: 'marker',
                  	coords: [38.900293, -77.038145],
                  	orientation: "WEST",
                  },
                  {
                  	id: 98,
                  	camId: '99',
                  	name: 'H St @ Vermont Ave & Madison Pl',
                  	type: 'marker',
                  	coords: [38.900124, -77.035025],
                  	orientation: "EAST",
                  },
                  {
                  	id: 99,
                  	camId: '100',
                  	name: '15th St @ New York Ave & Pennsylvania Ave',
                  	type: 'marker',
                  	coords: [38.898586, -77.033779],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 100,
                  	camId: '101',
                  	name: '14th St @ I St',
                  	type: 'marker',
                  	coords: [38.90123, -77.032121],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 101,
                  	camId: '102',
                  	name: '13th St @ I St',
                  	type: 'marker',
                  	coords: [38.901434, -77.029495],
                  	orientation: "NORTH",
                  },
                  {
                  	id: 102,
                  	camId: '103',
                  	name: '18th St @ I St',
                  	type: 'marker',
                  	coords: [38.901243, -77.041782],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 103,
                  	camId: '104',
                  	name: 'I St @ 17th St',
                  	type: 'marker',
                  	coords: [38.901273, -77.039281],
                  	orientation: "EAST",
                  },
                  {
                  	id: 104,
                  	camId: '105',
                  	name: 'I St @ 16th St',
                  	type: 'marker',
                  	coords: [38.901271, -77.036423],
                  	orientation: "EAST",
                  },
                  {
                  	id: 105,
                  	camId: '106',
                  	name: '13th St @ H St & New York Ave',
                  	type: 'marker',
                  	coords: [38.900007, -77.02976],
                  	orientation: "SOUTH",
                  },
                  {
                  	id: 106,
                  	camId: '107',
                  	name: 'K St @ 13th St',
                  	type: 'marker',
                  	coords: [38.9026, -77.029788],
                  	orientation: "WEST",
                  },
                  {
                  	id: 107,
                  	camId: '108',
                  	name: '15th St @ K St',
                  	type: 'marker',
                  	coords: [38.902393, -77.033758],
                  	orientation: "NORTH",
                  },
                  {
                  	id: 108,
                  	camId: '109',
                  	name: '15th St @ Pennsylvania Ave & E St',
                  	type: 'marker',
                  	coords: [38.895718, -77.0335],
                  	orientation: "NORTH",
                  },
                  {
                  	id: 109,
                  	camId: '110',
                  	name: 'Whitehaven St @ Massachusetts Ave',
                  	type: 'marker',
                  	coords: [38.918257, -77.05929],
                  	orientation: "EAST",
                  },
                  {
                  	id: 110,
                  	camId: '111',
                  	name: 'Canal Rd @ Chain Brdg Rd',
                  	type: 'marker',
                  	coords: [38.930399, -77.111757],
                  	orientation: "NORTH",
                  },
        ],
      },
    ],
  },
  mounted() {
    this.initMap();
    this.initLayers();
    this.layerChanged(0,true); //init the cameras on the map
    this.loadObject(0);
  },
  methods: {
    layerChanged(layerId, active) {
      const layer = this.layers.find(layer => layer.id === layerId);

      layer.features.forEach((feature) => {
        if (active) {
          feature.leafletObject.addTo(this.map);
        } else {
          feature.leafletObject.removeFrom(this.map);
        }
      });
    },
    initLayers() {
      this.layers.forEach((layer) => {
        const markerFeatures = layer.features.filter(feature => feature.type === 'marker');

        markerFeatures.forEach((feature) => {
          feature.leafletObject = L.marker(feature.coords)
            .bindPopup(feature.camId).on('click', onClick);
        });

        //need to parse out the event for high level data to pass to showImage
        function onClick(e) {
          // this.pic = this.getPopup().getContent();
          var camid = this.getPopup().getContent();
          vm.showImage(camid);
        }
      });
    },
    initMap() {
      this.map = L.map('map').setView([38.9, -77.04], 12);
      this.tileLayer = L.tileLayer(
        // 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png',
        'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        {
          maxZoom: 18,
          attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>',
        }
      );

      this.tileLayer.addTo(this.map);
    },
    loadObject(camid) {
      var new_camid = camid+1;
      var req = "http://127.0.0.1:5000/image?id="+new_camid;

      // console.log(req);
      axios.get(req).then(response => {
          this.results = response.data[0]
      })
    },
    showImage(camid) {
      // console.log(camid);
      var new_camid = camid;
      var req = "http://127.0.0.1:5000/image?id="+new_camid;

      axios.get(req).then(response => {
          this.results = response.data[response.data.length-1]
      })
      // console.log(this.results);
      //modifies fp to load images
      this.pic = this.results.filepath;
      //not being updated in line with the clicks -- check the initial load of objects
      this.updated_pic = this.results.datetime_readable;
      this.showAllImage(new_camid);
      this.imageSelected = true;
    },
    showAllImage(camid) {
      // console.log(camid);
      var new_camid = camid;
      var req = "http://127.0.0.1:5000/image?id="+new_camid;

      axios.get(req).then(response => {
          this.all_results = response.data
      })
      // console.log(this.results);
      //modifies fp to load images
      // this.pic = this.results.filepath;
      //not being updated in line with the clicks -- check the initial load of objects
      // this.updated_pic = this.results.datetime_readable;
      // this.imageSelected = true;
      // this.all_results =
    },
    getImage(fp) {
      // console.log(fp);
      // this.results.filepath = this.results.filepath.replace(".png","");
      // var new_fp = "../keras-yolo3/static/images/"+this.results.filepath+"_detected.png";

      // this is for testing the query and stats page for camera
      var new_fp = "/Users/fernab20/Documents/GWU/sd-20-fernandez-rood-shah/static/images/1/92_20200119_142420_detected.png";
      this.results.filepath = new_fp;
      return new_fp;
    },
  },
});
