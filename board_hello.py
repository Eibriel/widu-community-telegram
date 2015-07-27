board_hello = {
    'name': 'hello',
    'triggers': ['first_hi'],
    'nodes': [
        {
            'name': 'good_day',
            'text': [['¡Buen día!'], ['¡Buenos dias!']],
            'decoration': ['repeat_last_char'],
            'children': ['hello']
        },
        {
            'name': 'hello',
            'text': [['¡Hola!']],
            'children': ['who_are_you', 'what_is_hovyu', 'what_is_sustainable', 'where_cani_find_sustainable_stores', 'i_know_a_sustainable_store']
        },
        {
            'name': 'who_are_you',
            'text': [['¿Quién sos?']],
            'children': ['i_am_hovyu'],
            'if_not': ['know_hovyubot']
        },
        {
            'name': 'what_is_hovyu',
            'text': [['¿Qué significa Hovyũ?']],
            'children': ['hovyu_means'],
            'if': ['know_hovyubot'],
            'if_not': ['know_hovyu']
        },
        {
            'name': 'i_am_hovyu',
            'text': [['Soy Hovyũ, un bot verde', 'me interesa la sostenibilidad', 'si a vos también te interesa podemos charlar!']],
            'children': ['what_is_hovyu', 'what_is_sustainable', 'where_cani_find_sustainable_stores', 'i_know_a_sustainable_store'],
            'infer': ['know_hovyubot']
        },
        {
            'name': 'hovyu_means',
            'text': [['Hovyũ significa Verde en guaraní', 'se pronuncia Hoviú o Hovuú']],
            'children': ['who_are_you', 'what_is_sustainable', 'where_cani_find_sustainable_stores', 'i_know_a_sustainable_store'],
            'infer': ['know_hovyu']
        },
        {
            'name': 'what_is_sustainable',
            'text': [['¿Qué es sostenible?']],
            'children': ['sustainibility_is'],
            'if_not': ['know_sustainability']
        },
        {
            'name': 'where_cani_find_sustainable_stores',
            'text': [["¿Dónde encuentro comercios sostenibles?"]],
            'children': ['send_me_your_location_and_i_tell_you_green_stores_in_the_zone'],
            'if': ['know_sustainability']
        },
        {
            'name': 'i_know_a_sustainable_store',
            'text': [["Yo conozco un comercio sostenible"]],
            'children': ['great_join_the_group_and_comment_it'],
            'if': ['know_sustainability']
        },
        {
            'name': 'sustainibility_is',
            'text': [
                [
                    'Sostenibilidad (a veces llamado Sustentabilidad) conciste en satisfacer las necesidades de la actual generación sin sacrificar la capacidad de futuras generaciones de satisfacer sus propias necesidades.',
                    'Sueno como Wikipedia! 😜'
                ]
            ],
            'children': ['i_understand', 'i_dont_understand_sustainibility']
        },
        {
            'name': 'sustainibility_is_2',
            'text': [
                ['Es promover el progreso económico y social respetando los ecosistemas naturales y la calidad del medio ambiente.'],
                ['Hay que adoptar valores para mantener valores armónicos y satisfactorios de educación, capacitación y concientización.']],
            'children': ['i_understand', 'i_understand_not']
        },
        {
            'name': 'send_me_your_location_and_i_tell_you_green_stores_in_the_zone',
            'text': [
                [
                    'Enviame tu hubicación y te digo que comercios verdes hay por tu zona'
                ]
            ],
            'children': ['i_understand']
        },
        {
            'name': 'great_join_the_group_and_comment_it',
            'text': [
                [
                    'Genial! Unite al grupo https://telegram.me/joinchat/0338811e00225f1561463d99065a12d7 y comentalo!'
                ]
            ],
            'children': ['i_understand']
        },
        {
            'name': 'i_understand',
            'text': [['¡Entendido!']],
            'children': ['great'],
            'infer': ['know_sustainability']
        },
        {
            'name': 'i_dont_understand_sustainibility',
            'text': [['Sigo sin entender']],
            'children': ['sustainibility_is_2']
        },
        {
            'name': 'i_understand_not',
            'text': [['Entiendo... si... perfectamente...']],
            'children': ['dont_mok_me']
        },

        {
            'name': 'great',
            'text': [['¡Genial!'], ['¡Perfecto!']],
            'children': ['who_are_you', 'what_is_hovyu', 'what_is_sustainable', 'where_cani_find_sustainable_stores', 'i_know_a_sustainable_store']
        },
        {
            'name': 'dont_mok_me',
            'text': [['¡No te burles! 😡'], ['Si... seguro... 😒']],
            'children': ['who_are_you', 'what_is_hovyu', 'what_is_sustainable', 'where_cani_find_sustainable_stores', 'i_know_a_sustainable_store']
        }


    ]
}
