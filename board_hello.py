main = [
    'who_are_you',
    'what_is_hovyu',
    'what_is_sustainable',
    'good_day',
    'where_cani_find_sustainable_stores',
    'i_know_a_sustainable_store',
    'tell_me_more_about_sustainibility',
    'im_interested_on_sustainibility'
]

more_sustainibility = [
    'but_the_world_is_full_of_resources',
    'what_needs_change',
    'we_can_talk_later'
]

board_hello = {
    'name': 'hello',
    'triggers': ['first_hi'],
    'nodes': [
        {
            'name': 'good_day',
            'text': [['¡Buen día!'], ['¡Buenos dias!']],
            'children': ['hello']
        },
        {
            'name': 'hello',
            'text': [['¡Hola!'], ['¿Cómo andas?']],
            'decoration': ['repeat_last_char'],
            'children': main
        },
        {
            'name': 'who_are_you',
            'text': [['¿Quién eres?']],
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
            'text': [['Soy Hovyũ, un bot verde', 'me interesa la vida consciente', 'si a vos también te interesa podemos charlar!']],
            'children': main,
            'infer': ['know_hovyubot']
        },
        {
            'name': 'hovyu_means',
            'text': [['Hovyũ significa Verde en guaraní', 'se pronuncia Hoviú o Hovuú']],
            'children': main,
            'infer': ['know_hovyu']
        },
        {
            'name': 'im_interested_on_sustainibility',
            'text': [['¡Me interesa la vida consciente!']],
            'children': ['great'],
            'if': ['know_hovyubot'],
            'if_not': ['know_sustainability'],
            'infer': ['know_sustainability']
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
                    'Sostenibilidad (a veces llamado Sustentabilidad) consiste en satisfacer las necesidades de la actual generación sin sacrificar la capacidad de futuras generaciones de satisfacer sus propias necesidades.',
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
                    'Envíame tu ubicación, o escribe "zona NombreCiudad" y te diré que comercios verdes hay por tu zona. Por ejemplo "zona Bahía Blanca".'
                ]
            ],
            'children': ['i_understand_sustainibility']
        },
        {
            'name': 'great_join_the_group_and_comment_it',
            'text': [
                [
                    'Genial! Unete al grupo https://telegram.me/joinchat/0338811e00225f1561463d99065a12d7 y comentalo!'
                ]
            ],
            'children': ['i_understand']
        },
        {
            'name': 'i_understand_sustainibility',
            'text': [['¡Entendido!']],
            'children': ['great'],
            'infer': ['know_sustainability']
        },
        {
            'name': 'i_understand',
            'text': [['¡Entendido!']],
            'children': ['great'],
            #'infer': ['know_sustainability']
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
            'children': main
        },
        {
            'name': 'dont_mok_me',
            'text': [['¡No te burles! 😡'], ['Si... seguro... 😒']],
            'children': main
        },

        {
            'name': 'tell_me_more_about_sustainibility',
            'text': [['Cuéntame más acerca de sostenibilidad']],
            'children': ['more_sustainibility'],
            'if': ['know_sustainability']
        },
        {
            'name': 'more_sustainibility',
            'text': [['Necesitamos cambiar nuestra mentalidad, los modelos actuales están dejando ver sus fallas',
                'la población mundial crece en forma exponencial, y hay que pensar como dividirnos los recursos de la mejor manera posible',
                'pero ese cambio comienza por uno mismo, derrochar ya pasó de moda 😉'
            ]],
            'children': more_sustainibility,
        },
        {
            'name': 'we_can_talk_later',
            'text': [['Después seguimos hablando']],
            'children': ['great']
        },
        {
            'name': 'but_the_world_is_full_of_resources',
            'text': [['Pero el mundo está lleno de recursos!']],
            'children': ['we_need_to_manage_them_properly']
        },
        {
            'name': 'we_need_to_manage_them_properly',
            'text': [['Pero si se derrochan se van a terminar antes de que puedan recuperarse naturalmente',
                'de hecho actualmente en el mundo se consume en 6 meses los recursos de 1 año.']],
            'children': more_sustainibility
        },
        {
            'name': 'what_needs_change',
            'text': [['Qué cosas hacen falta cambiar?']],
            'children': ['we_need_to_change']
        },
        {
            'name': 'we_need_to_change',
            'text': [['Necesitamos entender que el dinero no tiene ningún valor',
                'los humanos no necesitamos dinero para vivir, necesitamos recursos.']],
            'children': ['we_need_money_to_buy_stuff', 'we_can_talk_later']
        },
        {
            'name': 'we_need_money_to_buy_stuff',
            'text': [['Necesitamos dinero para comer!']],
            'children': ['millonarie_island']
        },
        {
            'name': 'millonarie_island',
            'text': [['Imagínate que tienes una maleta con mucho dinero',
                'pero estás en una isla solitaria, sin frutos, peces, ni agua.',
                '¡El dinero no sirve de nada! Y la pobreza no se resuelve repartiendo dinero.']],
            'children': more_sustainibility
        },

    ]
}
