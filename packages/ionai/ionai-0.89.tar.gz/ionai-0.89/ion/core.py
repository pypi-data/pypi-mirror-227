#
# [name] ion.core.py
#
# Written by Yoshikazu NAKAJIMA
#

import sys
import json
import pprint  # リストや辞書を整形して出力
import datetime
from typing import Union
from nkj.str import *
import nkj.time as nt

ANYSTR = '_ANY'

NULL_SLOT = NULLSTR

_DEFAULT_NAMESPACE = 'https://www.tmd.ac.jp/bmi/'
_DEFAULT_SLOT = None
_DEFAULT_STRSLOT = NULL_SLOT

#-- global variance

__NAMESPACE = _DEFAULT_NAMESPACE

#-- global functions

def namespace(s=None):
	global __NAMESPACE
	if (s is None):
		return __NAMESPACE
	elif (type(s) is str):
		__NAMESPACE = s
		return True
	else:
		return False

def is_anystr(s:str):
	return True if (s == ANYSTR) else False

def anystr(s:str):
	return is_anystr(s)

def nullslot(slot):
	if (slot is None):
		return True
	else:
		return nullstr(slot)

def not_nullslot(slot):
	return not nullstr(slot)

def is_nullslot(slot):
	return nullslot(slot)

def isnot_nullslot(slot):
	return not_nullslot(slot)

def dictslot_equalsto(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 == dictslot2)

def dictslot_included(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 <= dictslot2)

def dictslot_includes(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 >= dictslot2)

def semantics_equalsto(sem1, sem2):
	if (sem1 is None):
		return False
	if (sem2 is None):
		return False

def nullslot(slot):
	if (slot is None):
		True
	return nullstr(slot)

def not_nullslot(slot):
	return not nullstr(slot)

def is_nullslot(slot):
	return nullslot(slot)

def isnot_nullslot(slot):
	return not_nullslot(slot)

def dictslot_equalsto(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 == dictslot2)

def dictslot_included(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 <= dictslot2)

def dictslot_includes(dictslot1, dictslot2):
	if (nullslot(dictslot1)):
		return True
	if (nullslot(dictslot2)):
		return True
	return (dictslot1 >= dictslot2)

def semantics_equalsto(sem1, sem2):
	if (sem1 is None):
		return False
	if (sem2 is None):
		return False
	return (sem1 == sem2)

def semantics_included(sem1, sem2):
	if (sem1 is None):
		return False
	if (sem2 is None):
		return False
	return (sem1 <= sem2)

def semantics_includes(sem1, sem2):
	if (sem1 is None):
		return False
	if (sem2 is None):
		return False
	return (sem1 >= sem2)

#-- classes

class core:
	_classname = 'ion.core'

	def __init__(self):
		ldprint2('core.__init__()')

	@classmethod
	def getClassName(cls):
		return core._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

class strslot(core, str):
	_classname = 'ion.strslot'

	def __new__(cls, val:str=_DEFAULT_STRSLOT):
		ldprint2('__new__()')
		val = NULL_SLOT if (val is None) else val
		self = super().__new__(cls, val)
		return self

	def __init__(self, val=_DEFAULT_STRSLOT):
		ldprint2('__init__()')
		super(core, self).__init__()

	def __eq__(self, second):
		if (type(second) == str):
			return True if (is_anystr(self.str) or is_anystr(second)) else (self.str == second)
		else:
			return True if (is_anystr(self.str) or is_anystr(second)) else (self.str == second.str)

	# __ne__() は実装しなくても、__eq__() から自動で実装されるので定義しない．

	def __lt__(self, second):
		if (is_anystr(self.str)):  # 自身が any なら True を返す．
			return True
		t = type(second)

		if (t == tuple or t == list):  # second がリストなら、要素に含まれるか判定
			ldprint2('this: \'{}\''.format(self.str))
			ldprint2('list: {}'.format(second))
			if (type(second[0]) == str):
				return self.str in second
			else:
				flag = False
				for slot in second:
					if (self.str == slot.str):
						flag = True
						break
				return flag
		elif (t == str):  # second が文字列なら、文字列の一部に含まれるか判定
			if (is_anystr(second)):  # 相手が any なら True を返す
				return True
			else:
				return (self.str in second) and self.__ne__(second)
		else:
			if (is_anystr(second.str)):  # 相手が any なら True を返す
				return True
			else:
				return (self.str in second.str) and self.__ne__(second)

	def __le__(self, second):
		return (self.__lt__(second) or self.__eq__(second))

	def __gt__(self, second):
		if (is_anystr(self.str)):  # 自身が any なら True を返す．
			return True
		if (type(second) == str):
			return (second in self.str) and self.__ne__(second)
		else:
			return (second.str in self.str) and self.__ne__(second)

	def __ge__(self, second):
		return (self.__gt__(second) or self.__eq__(second))

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	"""
	___NOT_IMPLEMENTED
	def set(self, val):
		ldprint('--> set(\'{}\')'.format(val))
		self = strslot(val)
		ldprint('<-- set()')
	"""

	def get(self):  # null 文字のとき、None へ変換．
		if (is_nullstr(self)):
			return None
		else:
			return self

	@property
	def str(self) -> str:  # string クラスへ強制変換
		return str(self)

	def equalsto(self, second):
		return self.__eq__(second)

	def not_equalto(self, second):
		return self.equalsto(second)

	def included(self, second):
		return self.__le__(second)

	def not_included(self, second):
		return not self.included(second)

	def includes(self, second):
		return self.__ge__(second)

	def not_includes(self, second):
		return not self.includes(second)

	def startswith(self, second):
		if (is_anystr(self.str)):
			return True
		if (type(second) == str):
			if (is_anystr(second)):
				return True
			return self.str.startswith(second)
		else:
			if (is_anystr(second.str)):
				return True
			return self.str.startswith(second.str)

	def endswith(self, second):
		if (is_anystr(self.str)):
			return True
		if (type(second) == str):
			if (is_anystr(second)):
				return True
			return self.str.endswith(second)
		else:
			if (is_anystr(second.str)):
				return True
			return self.str.endswith(second.str)

	def startsfor(self, second):
		if (is_anystr(self.str)):
			return True
		if (type(second) == str):
			if (is_anystr(second)):
				return True
			return second.startswith(self.str)
		else:
			if (is_anystr(second.str)):
				return True
			return second.str.startswith(self.str)

	def starts(self, second):
		return self.startsfor(second)

	def ends(self, second):
		if (is_anystr(self.str)):
			return True
		if (type(second) == str):
			if (is_anystr(second)):
				return True
			return second.endswith(self.str)
		else:
			if (is_anystr(second.str)):
				return True
			return second.str.endswith(self.str)

	def endsfor(self, second):
		return self.ends(second)

class slot(strslot):
	_classname = 'ion.slot'

	def __new__(cls, val=_DEFAULT_SLOT):
		return super().__new__(cls, val)

	def __init__(self, val=_DEFAULT_SLOT):
		super().__init__(val)

	@classmethod
	def getClassName(cls):
		return cls._classname

	def get(self):  # null 文字のとき、None へ変換．int および float のとき、それぞれ int、float へ変換．
		s = self
		if (s == ''):
			return None
		elif (is_intstr(s)):
			return int(s)
		elif (is_floatstr(s)):
			return float(s)
		else:
			return self

class dictslot(core, dict):
	_classname = 'ion.dictslot'

	def __init__(self, val:Union[dict, str, None]):
		self._dict = {} if (val is None) else (json.loads(val) if (type(val) == str) else val)
		self._filename = None

	# 一致性は、両方の辞書に共通する keys に対して、それらの values が全一致したとき（ただし、any 一致は認める）に一致とみなす
	# 片方のリストにある key がもう一方のリストにない時には、ない方のリスト要素を any とみなす = すなわち、「指定なし」＝any として、その key については一致とみなす

	def __eq__(self, second:Union[dict, str, None]):
		if (second is None):  # second が None なら True
			return True
		if (type(second) == str):
			second = json.loads(second)  # str -> dict
		if (is_nulldict(self) or is_nulldict(second)):  # どちらかの辞書に要素がなければ True
			return True
		anditems = [(key, value) for key, value in self.items() if (slot(self.get(key)) == slot(second.get(key)))]  # value を slot として一致性比較 = any 一致を認める
		if (is_nulllist(anditems)):
			return False
		else:
			return True

	def __lt__(self, second:Union[dict, str, None]):
		if (second is None):
			return False
		if (type(second) == str):
			second = json.loads(second)  # str -> dict
		if (is_nulldict(self) or is_nulldict(second)):  # どちらかの辞書に要素がなければ False
			return False
		anditems = [(key, value) for key, value in self.items() if (slot(self.get(key)) < slot(second.get(key)))]  # value を slot として被包含性比較 = any 包含を認める
		if (is_nulllist(anditems)):
			return False
		else:
			return True

	def __le__(self, second:Union[dict, str, None]):
		return (self.__lt__(second) or self.__eq__(second))

	def __gt__(self, second:Union[dict, str, None]):
		if (second is None):
			return False
		if (type(second) == str):
			second = json.loads(second)  # str -> dict
		if (is_nulldict(self) or is_nulldict(second)):  # どちらかの辞書に要素がなければ False
			return False
		anditems = [(key, value) for key, value in self.items() if (slot(self.get(key)) > slot(second.get(key)))]  # value を slot として包含性比較 = any 包含を認める
		if (is_nulllist(anditems)):
			return False
		else:
			return True

	def __ge__(self, second:Union[dict, str, None]):
		return (self.__gt__(second) or self.__eq__(second))

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def equalsto(self, second):
		return self.__eq__(second)

	def not_equalto(self, second):
		return self.equalsto(second)

	def included(self, second):
		return self.__le__(second)

	def not_included(self, second):
		return not self.included(second)

	def includes(self, second):
		return self.__ge__(second)

	def not_includes(self, second):
		return not self.includes(second)

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '--- {} ---\n'.format(title)
		s += json.dumps(self) + '\n'  # dict -> str
		if (title is not None):
			s += '---\n'
		return s

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.getPrintString()

	def print(self, title=None):
		if (title is not None):
			print('--- {} ---'.format(title))
		pprint.pprint(self.printstr)
		if (title is not None):
			print('---', flush=True)
		else:
			sys.stdout.flush()

	def setFilename(self, filename):
		self._filename = filename

	def getFilename(self):
		return self._filename

	@property
	def filename(self):
		return self.getFilename()

	@filename.setter
	def filename(self, filename):
		self.setFilename(filename)

	# json.{loads(), dumps()}: dict データと string データの変換
	# json.{load(), dump()}:   JSON ファイルの読み書き

	def load(self, filename=None):
		filename = self.getFilename() if (filename is None) else filename
		if (filename is None):
			return False
		with open(filename) as f:
			self = json.load(f)

	def save(self, filename=None):
		filename = self.getFilename() if (filename is None) else filename
		if (filename is None):
			return False
		with open(filename, 'wt') as f:  # テキストモードで書き出し
			json.dump(self, f)

_KEY_TIME = 'time'
_KEY_TIMEPERIOD = 'time_period'
_TIMEDESCRIPTION = '%Y-%m-%d %H:%M:%S.%f'

class sidslot(dictslot):  # spatial identifier
	_classname = 'ion.sidslot'

	def __init__(self, val:Union[dict, str, None]):
		super().__init__(val)

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

class tidslot(dictslot):  # temporal identifier
	_classname = 'ion.tidslot'

	def __init__(self, val:Union[dict, str, None]):
		super().__init__(val)
		if (self.time is None):
			self.update_time()

	"""
	def __lt__(self, second:sidslot):  # 記号の意味としては、本来は等価を含まないが、実装の都合上、ここでは含むものとする
		return self.__le__(second)
	"""

	def __le__(self, second:sidslot):
		return self.included(second)

	"""
	def __gt__(self, second:sidslot):  # 記号の意味としては、本来は等価を含まないが、実装の都合上、ここでは含むものとする
		return self.__ge__(second)
	"""

	def __ge__(self, second:sidslot):
		return self.includes(second)

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def time(self):
		return self.get(_KEY_TIME)

	@time.setter
	def time(self, t):
		if (t is None):
			del self[_KEY_TIME]
		else:
			self[_KEY_TIME] = t

	@property
	def timeperiod(self):
		return self.get(_KEY_TIMEPERIOD)

	@timeperiod.setter
	def timeperiod(self, tp):
		if (tp is None):
			del self[_KEY_TIMEPERIOD]
		else:
			self[_KEY_TIMEPERIOD] = tp

	def update_time(self):
		self.time = datetime.datetime.now().strftime(_TIMEDESCRIPTION)  # python datetime のデフォルト書式で記述

	def clear_timeperiod(self):
		self.timeperiod = None

	def included(self, second:sidslot):
		if (self.time is None or second.time is None):  # 記述がないときは any とみなして True
			return True
		if (is_anystr(self.time) or is_anystr(second.time)):  # どちらかが any のときは True. any は基本的には記述なしで対応するのでできるだけ使用しないこと．
			return True
		return (self == second) or (nt.time(self.time, self.timeperiod) <= nt.time(second.time, second.timeperiod))

	def includes(self, second:sidslot):
		if (self.time is None or second.time is None):  # 記述がないときは any とみなして True
			return True
		if (is_anystr(self.time) or is_anystr(second.time)):  # どちらかが any のときは True. any は基本的には記述なしで対応するのでできるだけ使用しないこと．
			return True
		return (self == second) or (nt.time(self.time, self.timeperiod) >= nt.time(second.time, second.timeperiod))

_KEY_DATAFORMAT = 'format'
_KEY_DATAUNIT = 'unit'

class datapropslot(dictslot):  # data properties
	_classname = 'ion.datapropslot'

	def __init__(self, val:Union[dict, str, None]):
		super().__init__(val)

	@classmethod
	def getClassName(cls):
		return dictslot._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def format(self):
		return self.get(_KEY_DATAFORMAT)

	@format.setter
	def format(self, f):
		if (f is None):
			del self[_KEY_DATAFORMAT]
		self[_KEY_DATAFORMAT] = f

	@property
	def unit(self):
		return self.get(_KEY_DATAUNIT)

	@unit.setter
	def unit(self, u):
		if (u is None):
			del self[_KEY_DATAUNIT]
		self[_KEY_DATAUNIT] = u

class databody(core):
	_classname = 'ion.databody'

	def __init__(self, val):
		self._data = None

	@classmethod
	def getClassName(cls):
		return databody._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def get(self):
		return self._data

	def set(self, d):
		if (type(d) is str):
			if (d == NULLSTR):
				d = None
		self._data = d

	@property
	def data(self):
		return self.get()

	@data.setter
	def data(self, d):
		self.set(d)

# [ref] https://fakatatuku.hatenablog.com/entry/2015/03/26/233024

class ClassProperty(property):
	pass

class PropertyMeta(type):
	def __new__(cls, name, bases, namespace):
		props = [(k, v) for k, v in namespace.items() if type(v) == ClassProperty]
		for k, v in props:
			setattr(cls, k, v)
			del namespace[k]
		return type.__new__(cls, name, bases, namespace)

class semantics():
	_classname = 'ion.semantics'

	def __init__(self, entity=None, baseentity=None, role=None, si=None, ti=None, opt=None):
		ldprint('--> semantics.__init__(\'{0}\', \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\')'.format(entity, baseentity, role, si, ti, opt))
		ldprint('entity:      \'{}\''.format(entity))
		ldprint('base entity: \'{}\''.format(baseentity))
		ldprint('role:        \'{}\''.format(role))
		ldprint('si:          \'{}\''.format(si))
		ldprint('ti:          \'{}\''.format(ti))
		ldprint('options:     \'{}\''.format(opt))
		self._entity = slot(entity)       # entity
		self._bentity = slot(baseentity)  # base entity (optional)
		self._role = slot(role)           # role
		self._si = sidslot(si)            # spatial identifier
		self._ti = tidslot(ti)            # temporal identifier
		self._optional = dictslot(opt)    # optional properties
		ldprint('<-- semantics.__init__()')

	def __str__(self, second):
		return self.getPrintString()

	def __eq__(self, second):
		r = True
		r &= (self.entity == second.entity)
		r &= (self.baseentity == second.baseentity)
		r &= (self.role == second.role)
		if (any(self.si)):
			r &= (self.si == second.si)
		if (any(self.ti)):
			r &= (self.ti == second.ti)
		if (any(self.optional)):
			r &= (self.optional == second.optional)
		return r

	def __lt__(self, second):
		return (self.__lt__(second) and not self.__eq__(second))

	def __le__(self, second):
		r = True
		r &= (self.entity <= second.entity)
		r &= (self.baseentity <= second.baseentity)
		r &= (self.role <= second.role)
		if (any(self.si)):
			r &= (self.si <= second.si)
		if (any(self.ti)):
			r &= (self.ti <= second.ti)
		if (any(self.optional)):
			r &= (self.optional <= second.optional)
		return r

	def __gt__(self, second):
		return (self.__gt__(second) and not self.__eq__(second))

	def __ge__(self, second):
		r = True
		r &= (self.entity >= second.entity)
		r &= (self.baseentity >= second.baseentity)
		r &= (self.role >= second.role)
		if (any(self.si)):
			r &= (self.si >= second.si)
		if (any(self.ti)):
			r &= (self.ti >= second.ti)
		if (any(self.optional)):
			r &= (self.optional >= second.optional)
		return r

	@classmethod
	def getClassName(cls):
		return semantics._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def namespace(self):
		return namespace()  # call global function

	@namespace.setter
	def namespace(self, ns):
		namespace(ns)  # call global function

	@property
	def ns(self):
		return self.namespace

	@ns.setter
	def ns(self, ns_):
		self.namespace = ns_

	@property
	def entity(self):
		return self._entity

	@entity.setter
	def entity(self, val:Union[str, None]):
		self._entity = val

	@property
	def e(self):
		return self._entity

	@e.setter
	def e(self, val:Union[str, None]):
		self._entity = val

	@property
	def baseentity(self):
		return self._bentity

	@baseentity.setter
	def baseentity(self, val:Union[str, None]):
		self._bentity = val

	@property
	def bentity(self):
		return self._bentity

	@bentity.setter
	def bentity(self, val:Union[str, None]):
		self._bentity = val

	@property
	def be(self):
		return self._bentity

	@be.setter
	def be(self, val:Union[str, None]):
		self._bentity = val

	@property
	def role(self):
		return self._role

	@role.setter
	def role(self, val:Union[str, None]):
		self._role = val

	@property
	def r(self):
		return self._role

	@r.setter
	def r(self, val:Union[str, None]):
		self._role = val

	@property
	def spatialidentifier(self):
		return self._si

	@property
	def si(self):
		return self._si

	@property
	def s(self):
		return self._si

	@property
	def temporalidentifier(self):
		return self._ti

	@property
	def ti(self):
		return self._ti

	@property
	def t(self):
		return self._ti

	@property
	def optionalidentifier(self):
		return self._optional

	@property
	def oi(self):
		return self._optional

	@property
	def optional(self):
		return self._optional

	@property
	def opt(self):
		return self._optional

	@property
	def o(self):
		return self._optional

	def equalsto(self, second):
		return self.__eq__(second)

	def not_equalto(self, second):
		return self.equalsto(second)

	def included(self, second):
		return self.__le__(second)

	def not_included(self, second):
		return not self.included(second)

	def includes(self, second):
		return self.__ge__(second)

	def not_includes(self, second):
		return not self.includes(second)

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '--- {} ---\n'.format(title)
		s += 'entity:      \'{}\'\n'.format(self.entity.str)
		s += 'base entity: \'{}\'\n'.format(self.baseentity.str)
		s += 'role:        \'{}\'\n'.format(self.role.str)
		if (any(self.si)):
			s += self.si.getPrintString('si')
		if (any(self.ti)):
			s += self.ti.getPrintString('ti')
		if (any(self.optional)):
			s += self.optional.getPrintString('optional')
		if (title is not None):
			s += '---\n'
		return s

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.getPrintString()

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

class data_storage(core):  # The class name of 'data' is prohibited and might be used in python system.
	_classname = 'ion.data'

	def __init__(self, body=None, property=None):
		ldprint('--> data.__init__(, {})'.format(property))
		super().__init__()
		self._body = databody(body)
		self._property = datapropslot(property)
		ldprint('<-- data.__init__()')

	@classmethod
	def getClassName(cls):
		return data_storage._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def namespace(self):
		return namespace()  # call global function

	@namespace.setter
	def namespace(self, ns):
		namespace(ns)  # call global function

	@property
	def ns(self):
		return self.namespace

	@ns.setter
	def ns(self, ns_):
		self.namespace = ns_

	@property
	def databody(self):
		return self._body.get()

	@databody.setter
	def databody(self, d):
		self._body.set(d)

	@property
	def dbody(self):
		return self.databody

	@dbody.setter
	def dbody(self, d):
		self.databody = d

	@property
	def db(self):
		return self.databody

	@db.setter
	def db(self, d):
		self.databody = d

	@property
	def body(self):
		return self.databody

	@body.setter
	def body(self, d):
		self.databody = d

	@property
	def b(self):
		return self.databody

	@b.setter
	def b(self, d):
		self.databody = d

	@property
	def dataproperty(self):
		return self._property

	@dataproperty.setter
	def dataproperty(self, p):
		self._property = p

	@property
	def dproperty(self):
		return self.dataproperty

	@dproperty.setter
	def dproperty(self, p):
		self.dataproperty = p

	@property
	def dp(self):
		return self._property

	@dp.setter
	def dp(self, p):
		self.dataproperty = p

	# 'property' is not available for the name of 'class property' in python

	@property
	def p(self):
		return self._property

	@p.setter
	def p(self, p_):
		self.dataproperty = p_

class ion(core):
	_classname = 'ion.ion'

	def __init__(self):
		self._semantics = semantics()
		self._data = data_storage()

	@classmethod
	def getClassName(cls):
		return ion._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def namespace(self):
		return namespace()  # call global function

	@namespace.setter
	def namespace(self, ns):
		namespace(ns)  # call global function

	@property
	def ns(self):
		return self.namespace

	@ns.setter
	def ns(self, ns_):
		self.namespace = ns_

	@property
	def semantics(self):
		return self._semantics

	@semantics.setter
	def semantics(self, s):
		self._semantics = s

	@property
	def s(self):
		return self.semantics

	@s.setter
	def s(self, s_):
		self.semantics = s_

	@property
	def data(self):
		return self._data

	@data.setter
	def data(self, d):
		self._data = d

	@property
	def d(self):
		return self._data

	@d.setter
	def d(self, d_):
		self._data = d_

	@property
	def entity(self):
		return self.s.entity

	@entity.setter
	def entity(self, e):
		self.s.entity = e

	@property
	def e(self):
		return self.entity

	@e.setter
	def e(self, e_):
		self.entity = e_

	@property
	def baseentity(self):
		return self.s.baseentity

	@baseentity.setter
	def baseentity(self, be):
		self.s.baseentity = be

	@property
	def bentity(self):
		return self.baseentity

	@bentity.setter
	def bentity(self, be):
		self.baseentity = be

	@property
	def be(self):
		return self.baseentity

	@be.setter
	def be(self, be_):
		self.baseentity = be_

	@property
	def role(self):
		return self.s.role

	@role.setter
	def role(self, r):
		self.s.role = r

	@property
	def r(self):
		return self.role

	@r.setter
	def r(self, r_):
		self.role = r_

	@property
	def spatialidentifier(self):
		return self.s.spatialidentifier

	@spatialidentifier.setter
	def spatialidentifier(self, si):
		self.s.spatialidentifier = si

	@property
	def si(self):
		return self.spatialidentifier

	@si.setter
	def si(self, si_):
		self.spatialidentifier = si_

	@property
	def temporalidentifier(self):
		return self.s.temporalidentifier

	@temporalidentifier.setter
	def temporalidentifier(self, ti):
		self.s.temporalidentifier = ti

	@property
	def ti(self):
		return self.temporalidentifier

	@ti.setter
	def ti(self, ti_):
		self.temporalidentifier = ti_

	@property
	def optional(self):
		return self.s.optional

	@optional.setter
	def optional(self, o):
		self.s.optional = o

	@property
	def opt(self):
		return self.optional

	@opt.setter
	def opt(self, o):
		self.optional = o

	@property
	def o(self):
		return self.optional

	@o.setter
	def o(self, o_):
		self.optional = o_

	@property
	def databody(self):
		return self.d.databody

	@databody.setter
	def databody(self, db):
		self.d.databody = db

	@property
	def dbody(self):
		return self.databody

	@dbody.setter
	def dbody(self, db):
		self.databody = db

	@property
	def db(self):
		return self.databody

	@db.setter
	def db(self, db_):
		self.databody = db_

	@property
	def dataproperty(self):
		return self.d.dataproperty

	@dataproperty.setter
	def dataproperty(self, dp):
		self.d.dataproperty = dp

	@property
	def dproperty(self):
		return self.dataproperty

	@dproperty.setter
	def dproperty(self, dp):
		self.dataproperty = dp

	@property
	def dp(self):
		return self.dataproperty

	@dp.setter
	def dp(self, dp_):
		self.dataproperty = dp_

#-- main

if (__name__ == '__main__'):
	_DEBUGLEVEL = 1
	lib_debuglevel(_DEBUGLEVEL)
	debuglevel(_DEBUGLEVEL)

	# namespace

	if (True):
		print('\n-- NAMESPACE --')
		dprint('namespace: \'{}\''.format(namespace()))
		namespace('test_namespace')
		dprint('namespace: \'{}\''.format(namespace()))

	# test for slot class

	if (False):
		print('\n-- SLOT CLASS --')
		sl = slot()
		dprint('classname: \'{}\''.format(sl.getClassName()))
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		print('\n--')
		sl = slot('test')
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		print('\n--')
		sl = slot('-30')
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		print('\n--')
		sl = slot('-3.14')
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		print('\n--')
		sl = slot('-3.14e+3')
		dprint('classname: \'{}\''.format(sl.classname))
		dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
		dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

		if (False):  # ___NOT_IMPLEMENTED
			print('\n-- test')
			sl.set('2.71828')
			dprint('classname: \'{}\''.format(sl.classname))
			dprint('slot:      \'{0}\' ({1})'.format(sl, type(sl)))
			dprint('slot:      \'{0}\' ({1})'.format(sl.str, type(sl.str)))
			dprint('slot:      \'{0}\' ({1})'.format(sl.get(), type(sl.get())))

	# test for semantics class

	if (True):
		print('\n-- SEMANTICS CLASS --')
		sem = semantics('test_ent_', None, None)
		dprint('classname: \'{}\''.format(sem.classname))
		sem.print('semantics')

		print('\n--')
		dprint('namespace: \'{}\''.format(sem.namespace))
		sem.namespace = 'test_namespace2'
		dprint('namespace: \'{}\''.format(sem.namespace))
		sem.ns = 'test_namespace3'
		dprint('namespace: \'{}\''.format(sem.ns))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.entity.classname))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity, type(sem.entity)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.str, type(sem.entity.str)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.get(), type(sem.entity.get())))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.entity.classname))
		sem.entity = slot('test_ent')  # 代入時は必ず slot 形式にキャストしてから代入すること．直接、string データを代入すると、sem.entity が string 型になってしまう。
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity, type(sem.entity)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.str, type(sem.entity.str)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.get(), type(sem.entity.get())))
		if (True):
			dprint('Is equal to \'{0}\': {1}'.format('test_entXXX', sem.entity == 'test_ent/XXX'))
			dprint('Is equal to \'{0}\': {1}'.format('test_ent', sem.entity == 'test_ent'))
			dprint('Is equal to \'{0}\': {1}'.format('test_e', sem.entity == 'test_e'))
			dprint('Is equal to \'{0}\': {1}'.format('dummy', sem.entity == 'dummy'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_ent/XXX', sem.entity != 'test_ent/XXX'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_ent', sem.entity != 'test_ent'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_e', sem.entity != 'test_e'))
			dprint('Is not equal to \'{0}\': {1}'.format('dummy', sem.entity != 'dummy'))
			dprint('Is included in \'{0}\': {1}'.format('test_ent/XXX', sem.entity < 'test_ent/XXX'))
			dprint('Is included in \'{0}\': {1}'.format('test_ent', sem.entity < 'test_ent'))
			dprint('Is included in \'{0}\': {1}'.format('test_e', sem.entity < 'test_e'))
			dprint('Is included in \'{0}\': {1}'.format('dummy', sem.entity < 'dummy'))
			dprint('Is included in \'{0}\': {1}'.format(['dummy'], sem.entity < ['dummy']))
			dprint('Is included in \'{0}\': {1}'.format('[\'test_ent\', \'dummy\']', sem.entity < ['test_ent', 'dummy']))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_ent/XXX', sem.entity <= 'test_ent/XXX'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_ent', sem.entity <= 'test_ent'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_e', sem.entity <= 'test_e'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('dummy', sem.entity <= 'dummy'))
			dprint('Does include \'{0}\': {1}'.format('test_ent/XXX', sem.entity > 'test_ent/XXX'))
			dprint('Does include \'{0}\': {1}'.format('test_ent', sem.entity > 'test_ent'))
			dprint('Does include \'{0}\': {1}'.format('test_e', sem.entity > 'test_e'))
			dprint('Does include \'{0}\': {1}'.format('dummy', sem.entity > 'dummy'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_ent/XXX', sem.entity >= 'test_ent/XXX'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_ent', sem.entity >= 'test_ent'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_e', sem.entity >= 'test_e'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('dummy', sem.entity >= 'dummy'))
			dprint('Does start with \'{0}\': {1}'.format('test_ent/XXX', sem.entity.startswith('test_ent/XXX')))
			dprint('Does start with \'{0}\': {1}'.format('test_ent', sem.entity.startswith('test_ent')))
			dprint('Does start with \'{0}\': {1}'.format('test_e', sem.entity.startswith('test_e')))
			dprint('Does start with \'{0}\': {1}'.format('dummy', sem.entity.startswith('dummy')))
			dprint('Does start for \'{0}\': {1}'.format('test_ent/XXX', sem.entity.starts('test_ent/XXX')))
			dprint('Does start for \'{0}\': {1}'.format('test_ent', sem.entity.starts('test_ent')))
			dprint('Does start for \'{0}\': {1}'.format('test_e', sem.entity.starts('test_e')))
			dprint('Does start for \'{0}\': {1}'.format('dummy', sem.entity.starts('dummy')))
			dprint('Does end with \'{0}\': {1}'.format('XXX/test_ent', sem.entity.endswith('XXX/test_ent')))
			dprint('Does end with \'{0}\': {1}'.format('test_ent', sem.entity.endswith('test_ent')))
			dprint('Does end with \'{0}\': {1}'.format('test_e', sem.entity.endswith('test_e')))
			dprint('Does end with \'{0}\': {1}'.format('dummy', sem.entity.endswith('dummy')))
			dprint('Does end \'{0}\': {1}'.format('XXX/test_ent', sem.entity.ends('XXX/test_ent')))
			dprint('Does end \'{0}\': {1}'.format('test_ent', sem.entity.ends('test_ent')))
			dprint('Does end \'{0}\': {1}'.format('test_e', sem.entity.ends('test_e')))
			dprint('Does end \'{0}\': {1}'.format('dummy', sem.entity.ends('dummy')))

		print('\n--')
		sem.entity = slot(ANYSTR)  # 代入時は必ず slot 形式にキャストしてから代入すること．直接、string データを代入すると、sem.entity が string 型になってしまう。
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity, type(sem.entity)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.str, type(sem.entity.str)))
		dprint('entity:    \'{0}\' ({1})'.format(sem.entity.get(), type(sem.entity.get())))
		if (True):
			dprint('Is equal to \'{0}\': {1}'.format('test_entXXX', sem.entity == 'test_ent/XXX'))
			dprint('Is equal to \'{0}\': {1}'.format('test_ent', sem.entity == 'test_ent'))
			dprint('Is equal to \'{0}\': {1}'.format('test_e', sem.entity == 'test_e'))
			dprint('Is equal to \'{0}\': {1}'.format('dummy', sem.entity == 'dummy'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_ent/XXX', sem.entity != 'test_ent/XXX'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_ent', sem.entity != 'test_ent'))
			dprint('Is not equal to \'{0}\': {1}'.format('test_e', sem.entity != 'test_e'))
			dprint('Is not equal to \'{0}\': {1}'.format('dummy', sem.entity != 'dummy'))
			dprint('Is included in \'{0}\': {1}'.format('test_ent/XXX', sem.entity < 'test_ent/XXX'))
			dprint('Is included in \'{0}\': {1}'.format('test_ent', sem.entity < 'test_ent'))
			dprint('Is included in \'{0}\': {1}'.format('test_e', sem.entity < 'test_e'))
			dprint('Is included in \'{0}\': {1}'.format('dummy', sem.entity < 'dummy'))
			dprint('Is included in \'{0}\': {1}'.format(['dummy'], sem.entity < ['dummy']))
			dprint('Is included in \'{0}\': {1}'.format('[\'test_ent\', \'dummy\']', sem.entity < ['test_ent', 'dummy']))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_ent/XXX', sem.entity <= 'test_ent/XXX'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_ent', sem.entity <= 'test_ent'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('test_e', sem.entity <= 'test_e'))
			dprint('Is equal to or included in \'{0}\': {1}'.format('dummy', sem.entity <= 'dummy'))
			dprint('Does include \'{0}\': {1}'.format('test_ent/XXX', sem.entity > 'test_ent/XXX'))
			dprint('Does include \'{0}\': {1}'.format('test_ent', sem.entity > 'test_ent'))
			dprint('Does include \'{0}\': {1}'.format('test_e', sem.entity > 'test_e'))
			dprint('Does include \'{0}\': {1}'.format('dummy', sem.entity > 'dummy'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_ent/XXX', sem.entity >= 'test_ent/XXX'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_ent', sem.entity >= 'test_ent'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('test_e', sem.entity >= 'test_e'))
			dprint('Is equal to or does include \'{0}\': {1}'.format('dummy', sem.entity >= 'dummy'))
			dprint('Does start with \'{0}\': {1}'.format('test_ent/XXX', sem.entity.startswith('test_ent/XXX')))
			dprint('Does start with \'{0}\': {1}'.format('test_ent', sem.entity.startswith('test_ent')))
			dprint('Does start with \'{0}\': {1}'.format('test_e', sem.entity.startswith('test_e')))
			dprint('Does start with \'{0}\': {1}'.format('dummy', sem.entity.startswith('dummy')))
			dprint('Does start for \'{0}\': {1}'.format('test_ent/XXX', sem.entity.starts('test_ent/XXX')))
			dprint('Does start for \'{0}\': {1}'.format('test_ent', sem.entity.starts('test_ent')))
			dprint('Does start for \'{0}\': {1}'.format('test_e', sem.entity.starts('test_e')))
			dprint('Does start for \'{0}\': {1}'.format('dummy', sem.entity.starts('dummy')))
			dprint('Does end with \'{0}\': {1}'.format('XXX/test_ent', sem.entity.endswith('XXX/test_ent')))
			dprint('Does end with \'{0}\': {1}'.format('test_ent', sem.entity.endswith('test_ent')))
			dprint('Does end with \'{0}\': {1}'.format('test_e', sem.entity.endswith('test_e')))
			dprint('Does end with \'{0}\': {1}'.format('dummy', sem.entity.endswith('dummy')))
			dprint('Does end \'{0}\': {1}'.format('XXX/test_ent', sem.entity.ends('XXX/test_ent')))
			dprint('Does end \'{0}\': {1}'.format('test_ent', sem.entity.ends('test_ent')))
			dprint('Does end \'{0}\': {1}'.format('test_e', sem.entity.ends('test_e')))
			dprint('Does end \'{0}\': {1}'.format('dummy', sem.entity.ends('dummy')))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.bentity.classname))
		dprint('bentity:   \'{0}\' ({1})'.format(sem.bentity, type(sem.bentity)))
		dprint('bentity:   \'{0}\' ({1})'.format(sem.bentity.str, type(sem.bentity.str)))
		dprint('bentity:   \'{0}\' ({1})'.format(sem.bentity.get(), type(sem.bentity.get())))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.role.classname))
		dprint('role:      \'{0}\' ({1})'.format(sem.role, type(sem.role)))
		dprint('role:      \'{0}\' ({1})'.format(sem.role.str, type(sem.role.str)))
		dprint('role:      \'{0}\' ({1})'.format(sem.role.get(), type(sem.role.get())))

		print('\n--')
		dprint('classname: \'{}\''.format(sem.si.classname))
		dprint('si:      \'{0}\' ({1})'.format(sem.si, type(sem.si)))
		dprint('si:      \'{0}\' ({1})'.format(sem.si.printstr, type(sem.si.printstr)))
		dprint('si:      \'{0}\' ({1})'.format(sem.si.pstr, type(sem.si.pstr)))
		if (True):
			sem.si.print()
			sem.si.print('si')
		if (True):
			sem.si['format'] = 'tmdu/bmi/nakajima'
			sem.si['unit'] = 'radian'
			sem.si['time'] = {'time': '2023/08/22,21:12:27', 'period': '60', 'period_unit': 'seconds'}
			pprint.pprint(sem.si)
			sem.si.save('test.json')
			sem.si.load('test.json')
			sem.si.print('\'test.json\'')
			print('-- json.dumps() --')
			print(json.dumps(sem.si))
			print('--', flush=True)
			print('-- pprint.pprint() --')
			pprint.pprint(sem.si, indent=1, width=1)
			print('--', flush=True)

		print('\n--')
		dprint('classname: \'{}\''.format(sem.ti.classname))
		dprint('ti:      \'{0}\' ({1})'.format(sem.ti, type(sem.ti)))
		dprint('ti:      \'{0}\' ({1})'.format(sem.ti.printstr, type(sem.ti.printstr)))
		dprint('ti:      \'{0}\' ({1})'.format(sem.ti.pstr, type(sem.ti.pstr)))

	# test for data class

	if (True):
		print('\n-- DATA(_STORAGE) CLASS --')
		data = data_storage()
		dprint('classname: \'{}\''.format(data.classname))

	# test for ion class

	if (True):
		print('\n-- iON CLASS --')
		ion = ion()
		dprint('classname: \'{}\''.format(ion.classname))
